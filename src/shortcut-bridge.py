import os
import atexit,fcntl,json,re,subprocess,time,urllib.request
from pathlib import Path
import dbus,dbus.mainloop.glib
from gi.repository import GLib
from PySide6.QtGui import QKeySequence
from websockets.sync.client import connect
CDP_PORT=int(os.environ.get('GE_OVERLAY_CDP_PORT','9340'))
state=Path(os.environ.get('GE_OVERLAY_STATE_DIR',str(Path.home()/'.local/state/german-eiland-overlay-linux')));state.mkdir(parents=True,exist_ok=True)
lock=(state/'shortcut-bridge.lock').open('w')
try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
except BlockingIOError:raise SystemExit(0)
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True);bus=dbus.SessionBus()
api=dbus.Interface(bus.get_object('org.kde.kglobalaccel','/kglobalaccel'),'org.kde.KGlobalAccel')
component='german-eiland-overlay-linux';registered={};current={};socket=None;seq=0;misses=0;ptt_held=False
labels={'toggle':'Mostrar ou ocultar overlay','combat':'Bloquear cliques no overlay','ptt':'Falar enquanto segura','mute':'Silenciar microfone','menu':'Mostrar menu','lock':'Travar layout','settings':'Abrir configurações','deafen':'Silenciar áudio recebido','map':'Abrir mapa','toggle2':'Mostrar overlay (segunda tecla)'}
def aid(action):return dbus.Array([component,action,'German Eiland Overlay',labels.get(action,action)],signature='s')
def call(expression):
 global socket,seq
 try:
  if socket is None:
   ts=json.load(urllib.request.urlopen(f'http://127.0.0.1:{CDP_PORT}/json',timeout=2));t=next(t for t in ts if t['url']=='ovl3://overlay/index.html');socket=connect(t['webSocketDebuggerUrl'],open_timeout=2,max_size=20000000)
  seq+=1;socket.send(json.dumps({'id':seq,'method':'Runtime.evaluate','params':{'expression':expression,'returnByValue':True,'awaitPromise':True}}))
  while True:
   r=json.loads(socket.recv(timeout=3))
   if r.get('id')==seq:
    if 'exceptionDetails' in r.get('result',{}):raise RuntimeError(r['result']['exceptionDetails'].get('text'))
    return r.get('result',{}).get('result',{}).get('value')
 except Exception:
  if socket:
   try:socket.close()
   except Exception:pass
  socket=None;raise

def cleanup():
 global ptt_held
 if ptt_held:
  try:call('VOICE.ptt(false)')
  except Exception:pass
  ptt_held=False
 for action in list(registered):
  try:api.unregister(component,action)
  except Exception:pass
 registered.clear()
atexit.register(cleanup)
def focused_game():
 try:
  active=subprocess.check_output(['xprop','-root','_NET_ACTIVE_WINDOW'],text=True);m=re.search(r'0x[0-9a-f]+',active)
  if not m:return False
  cls=subprocess.check_output(['xprop','-id',m.group(),'WM_CLASS'],text=True)
  return 'steam_app_376210' in cls
 except Exception:return False

def fire(comp,action,timestamp,down=True):
 global ptt_held
 action=str(action)
 if str(comp)!=component or (not down and action!='ptt'):return
 expressions={
 'toggle':"S.mode.visible?N.ui.hide():N.ui.show()",
 'toggle2':"S.mode.visible?N.ui.hide():N.ui.show()",
 'combat':"N.ui.setCombat(!S.mode.combat)",
 'ptt':f"VOICE.ptt({str(down).lower()})",
 'mute':"VOICE.muteToggle()",'menu':"toggleMenu()",'lock':"toggleLock()",'settings':"toggleSettings()",'deafen':"VOICE.deafenToggle()",'map':"toggleMapTab()"}
 if action not in expressions:return
 try:
  call("(async()=>{if(REBIND||typingInOverlay())return;await ("+expressions[action]+");return true})()")
  if action=='ptt':ptt_held=down
  print('shortcut',action,'pressed' if down else 'released',flush=True)
 except Exception as e:print('shortcut error',type(e).__name__,str(e)[:140],flush=True)
bus.add_signal_receiver(fire,signal_name='globalShortcutPressed',dbus_interface='org.kde.kglobalaccel.Component',bus_name='org.kde.kglobalaccel')
bus.add_signal_receiver(lambda a,b,c:fire(a,b,c,False),signal_name='globalShortcutReleased',dbus_interface='org.kde.kglobalaccel.Component',bus_name='org.kde.kglobalaccel')
def poll():
 global current,misses
 try:
  data=json.loads(call("JSON.stringify({keys:HK(),capturing:REBIND!==null})"));misses=0
  wanted=data['keys'] if focused_game() and not data['capturing'] else {}
  # Leave local keyboard handling intact while the overlay itself has focus.
  for action in list(registered):
   if action not in wanted or wanted[action]!=registered[action]:
    if action=='ptt':
     call('VOICE.ptt(false)')
    api.unregister(component,action);registered.pop(action)
  for action,key in wanted.items():
   if action in registered or action not in labels:continue
   seqkey=QKeySequence.fromString(key);code=seqkey[0].toCombined() if not seqkey.isEmpty() else 0
   if not code:continue
   if not api.isGlobalShortcutAvailable(dbus.Int32(code),component):
    print('shortcut conflict',action,key,flush=True);continue
   api.doRegister(aid(action));result=api.setShortcut(aid(action),dbus.Array([code],signature='i'),dbus.UInt32(6))
   if code in result:registered[action]=key;print('registered',action,key,flush=True)
  current=wanted
 except Exception as e:
  misses+=1
  if misses==1:print('waiting for overlay',type(e).__name__,str(e)[:140],flush=True)
  cleanup()
  if misses>=30:loop.quit();return False
 return True
loop=GLib.MainLoop();GLib.timeout_add(500,poll);poll()
try:loop.run()
finally:cleanup()
