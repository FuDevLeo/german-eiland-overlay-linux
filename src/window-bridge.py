import asyncio, base64, ctypes as C, fcntl, io, json, os, re, subprocess, time, urllib.request
from pathlib import Path
from PIL import Image, ImageChops, ImageFilter, ImageDraw
import websockets
CDP_PORT=int(os.environ.get('GE_OVERLAY_CDP_PORT','9340'))
state=Path(os.environ.get('GE_OVERLAY_STATE_DIR',str(Path.home()/'.local/state/german-eiland-overlay-linux')));state.mkdir(parents=True,exist_ok=True)
lock=(state/'window-bridge.lock').open('w')
try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
except BlockingIOError: raise SystemExit(0)
x=C.CDLL('libX11.so.6');sx=C.CDLL('libXext.so.6')
x.XOpenDisplay.argtypes=[C.c_char_p];x.XOpenDisplay.restype=C.c_void_p
x.XCreateBitmapFromData.argtypes=[C.c_void_p,C.c_ulong,C.c_char_p,C.c_uint,C.c_uint];x.XCreateBitmapFromData.restype=C.c_ulong
x.XFreePixmap.argtypes=[C.c_void_p,C.c_ulong];x.XFlush.argtypes=[C.c_void_p]
sx.XShapeCombineMask.argtypes=[C.c_void_p,C.c_ulong,C.c_int,C.c_int,C.c_int,C.c_ulong,C.c_int]
x.XUnmapWindow.argtypes=[C.c_void_p,C.c_ulong]
x.XMapWindow.argtypes=[C.c_void_p,C.c_ulong]
d=x.XOpenDisplay(None)
if not d: raise SystemExit('No X display')
def win():
 r=subprocess.check_output(['xprop','-root','_NET_CLIENT_LIST'],text=True)
 for w in re.findall(r'0x[0-9a-f]+',r):
  s=subprocess.check_output(['xprop','-id',w,'WM_NAME','WM_CLASS'],text=True)
  if 'German Eiland Overlay' in s and 'steam_app_0' in s:return int(w,16)
 return None
async def fix_shop_selects():
 try:
  pages=json.load(urllib.request.urlopen(f'http://127.0.0.1:{CDP_PORT}/json',timeout=1))
  script=Path(__file__).resolve().with_name('shop-select-fix.js').read_text()
  for page in pages:
   if not page.get('url','').startswith('https://germaneiland.com/shop/'):continue
   async with websockets.connect(page['webSocketDebuggerUrl'],open_timeout=1,close_timeout=1) as ws:
    await ws.send(json.dumps({'id':1,'method':'Runtime.evaluate','params':{'expression':script}}))
    while True:
     r=json.loads(await asyncio.wait_for(ws.recv(),2))
     if r.get('id')==1:break
 except Exception:pass

async def main():
 missing=0;seq=0;last_shop=0
 while missing<30:
  try:
   ts=json.load(urllib.request.urlopen(f'http://127.0.0.1:{CDP_PORT}/json',timeout=2));target=next(t for t in ts if t['url']=='ovl3://overlay/index.html');wid=win()
   if not wid:raise RuntimeError('waiting for overlay window')
   subprocess.run(['xprop','-id',hex(wid),'-f','_NET_WM_WINDOW_TYPE','32a','-set','_NET_WM_WINDOW_TYPE','_KDE_NET_WM_WINDOW_TYPE_CRITICAL_NOTIFICATION'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
   # KWin updates the window category when it is remapped.
   x.XUnmapWindow(d,wid);x.XFlush(d);await asyncio.sleep(.15);x.XMapWindow(d,wid);x.XFlush(d)
   async with websockets.connect(target['webSocketDebuggerUrl'],max_size=20000000) as ws:
    async def call(method,params):
     nonlocal seq
     seq+=1;await ws.send(json.dumps({'id':seq,'method':method,'params':params}))
     while True:
      r=json.loads(await asyncio.wait_for(ws.recv(),8))
      if r.get('id')==seq:
       if 'error' in r:raise RuntimeError(r['error'])
       return r['result']
    await call('Runtime.evaluate',{'expression':"(()=>{let s=document.getElementById('ge-linux-clean-edges');if(!s){s=document.createElement('style');s.id='ge-linux-clean-edges';document.head.appendChild(s)}s.textContent='.fw-win,.d3-w{box-shadow:none!important}';})()"})
    while True:
     started=time.monotonic()
     if started-last_shop>5:
      await fix_shop_selects();last_shop=started
     # Chromium's own capture includes newly opened panels beyond the old X shape.
     r=await call('Page.captureScreenshot',{'format':'png','fromSurface':True,'captureBeyondViewport':False})
     im=Image.open(io.BytesIO(base64.b64decode(r['data']))).convert('RGB')
     rr,gg,bb=im.split();mask=ImageChops.lighter(ImageChops.lighter(rr,gg),bb).point(lambda v:255 if v>8 else 0).filter(ImageFilter.MaxFilter(3))
     rects=await call('Runtime.evaluate',{'expression':"JSON.stringify([...document.querySelectorAll('#top,#drop')].filter(e=>!e.hidden&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).visibility!=='hidden').map(e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}))",'returnByValue':True})
     draw=ImageDraw.Draw(mask)
     for box in json.loads(rects['result']['value']):
      if box[2]>box[0] and box[3]>box[1]:draw.rectangle(tuple(int(v) for v in box),fill=255)
     mask=mask.convert('1');data=mask.tobytes('raw','1;R');pix=x.XCreateBitmapFromData(d,wid,data,*im.size)
     if not pix:raise RuntimeError('could not create overlay mask')
     sx.XShapeCombineMask(d,wid,0,0,0,pix,0)
     mode=await call('Runtime.evaluate',{'expression':'Boolean(S.mode.combat||S.mode.locked)','returnByValue':True})
     if mode['result'].get('value'):
      empty=x.XCreateBitmapFromData(d,wid,b'\x00',1,1)
      sx.XShapeCombineMask(d,wid,2,0,0,empty,0);x.XFreePixmap(d,empty)
     else:sx.XShapeCombineMask(d,wid,2,0,0,pix,0)
     x.XFreePixmap(d,pix);x.XFlush(d)
     missing=0
     await asyncio.sleep(max(.1,.5-(time.monotonic()-started)))
  except Exception as e:
   missing+=1
   print(type(e).__name__,str(e)[:180],flush=True)
   await asyncio.sleep(1)
asyncio.run(main())
