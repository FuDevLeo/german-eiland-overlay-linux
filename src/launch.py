"""Launcher for the separately obtained official overlay; no user profile is bundled."""
import argparse
import ctypes
import importlib
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import time

SOURCE = Path(__file__).resolve().parent
CONFIG = Path(os.environ.get('XDG_CONFIG_HOME', Path.home()/'.config'))/'german-eiland-overlay-linux/config.json'
DATA = Path(os.environ.get('XDG_DATA_HOME', Path.home()/'.local/share'))/'german-eiland-overlay-linux'
STATE = Path(os.environ.get('XDG_STATE_HOME', Path.home()/'.local/state'))/'german-eiland-overlay-linux'

def dependencies():
    errors=[]
    for module in ['PIL.Image','websockets','websockets.sync.client','dbus','gi.repository.GLib','PySide6.QtGui']:
        try: importlib.import_module(module)
        except ImportError: errors.append('Missing Python module: '+module)
    for library in ['libX11.so.6','libXext.so.6']:
        try: ctypes.CDLL(library)
        except OSError: errors.append('Missing library: '+library)
    if not shutil.which('xprop'): errors.append('Missing command: xprop')
    if not os.environ.get('DISPLAY'): errors.append('DISPLAY is not set; X11/Xwayland is required')
    if not os.environ.get('DBUS_SESSION_BUS_ADDRESS'): errors.append('A desktop D-Bus session is required')
    if errors: raise SystemExit('\n'.join(errors))

def find_proton():
    for steam in [Path.home()/'.local/share/Steam',Path.home()/'.steam/steam']:
        candidate=steam/'steamapps/common/Proton - Experimental/proton'
        if candidate.is_file(): return candidate
    return None

def load_config():
    if not CONFIG.exists(): return {}
    return json.loads(CONFIG.read_text())

def save_shortcut(exe,proton):
    CONFIG.parent.mkdir(parents=True,exist_ok=True)
    CONFIG.write_text(json.dumps({'exe':str(exe),'proton':str(proton)},indent=2)+'\n')
    CONFIG.chmod(0o600)
    apps=Path(os.environ.get('XDG_DATA_HOME',Path.home()/'.local/share'))/'applications'
    apps.mkdir(parents=True,exist_ok=True)
    launcher=SOURCE.parent/'launch.sh'
    quoted='"'+str(launcher).replace('\\','\\\\').replace('"','\\"').replace('`','\\`').replace('$','\\$').replace('%','%%')+'"'
    (apps/'german-eiland-overlay-linux.desktop').write_text('[Desktop Entry]\nType=Application\nName=German Eiland Overlay (Linux prototype)\nComment=Unofficial Linux compatibility launcher\nExec=/usr/bin/bash '+quoted+'\nIcon=applications-games\nTerminal=false\nCategories=Game;\n')
    print('Saved a local configuration and application-menu shortcut. Keep this source folder in place.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe',type=Path,help='Path to your official installed German Eiland Overlay.exe')
    parser.add_argument('--proton',type=Path,help='Path to the existing Proton Experimental/proton script')
    parser.add_argument('--check',action='store_true',help='Check dependencies without starting Wine, the overlay or the game')
    parser.add_argument('--install-shortcut',action='store_true',help='Save paths locally and add an application-menu shortcut, without starting anything')
    parser.add_argument('--port',type=int,default=9340,help='Loopback-only Chromium debugging port (default: 9340)')
    args=parser.parse_args()
    if args.check:
        dependencies();print('Dependencies available. This does not verify interactive behavior.');return
    cfg=load_config()
    exe=args.exe or (Path(cfg['exe']) if cfg.get('exe') else None)
    proton=args.proton or (Path(cfg['proton']) if cfg.get('proton') else find_proton())
    if exe is None or not exe.expanduser().is_file():parser.error('Provide --exe with the official installed overlay executable; the full application folder is required.')
    if proton is None or not proton.expanduser().is_file():parser.error('Install Proton Experimental in Steam or provide --proton.')
    exe=exe.expanduser().resolve();proton=proton.expanduser().resolve()
    if args.install_shortcut:save_shortcut(exe,proton);return
    dependencies()
    if not 1024<=args.port<=65535:parser.error('--port must be between 1024 and 65535')
    with socket.socket() as probe:
        try:probe.bind(('127.0.0.1',args.port))
        except OSError:parser.error('The debugging port is in use. Close the previous overlay or choose another --port; this launcher will not attach to an unknown process.')
    compat=DATA/'compatdata';compat.mkdir(parents=True,exist_ok=True);STATE.mkdir(parents=True,exist_ok=True)
    steam=proton.parent.parent.parent.parent
    env=os.environ.copy()
    env.update(STEAM_COMPAT_DATA_PATH=str(compat),STEAM_COMPAT_CLIENT_INSTALL_PATH=str(steam),SteamAppId='0',SteamGameId='0',GE_OVERLAY_STATE_DIR=str(STATE),GE_OVERLAY_CDP_PORT=str(args.port))
    children=[]
    def stop(*_):
        for child in reversed(children):
            if child.poll() is None:
                try:os.killpg(child.pid,signal.SIGTERM)
                except ProcessLookupError:pass
    signal.signal(signal.SIGINT,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    try:
        with (STATE/'launch.log').open('a') as log:
            app=subprocess.Popen([str(proton),'run',str(exe),'--remote-debugging-address=127.0.0.1',f'--remote-debugging-port={args.port}'],env=env,stdout=log,stderr=log,start_new_session=True)
            children.append(app)
            for name in ['window-bridge.py','shortcut-bridge.py']:
                child=subprocess.Popen([sys.executable,str(SOURCE/name)],env=env,stdout=log,stderr=log,start_new_session=True);children.append(child)
            print('Overlay launched. F7 toggles mouse interaction; helper logs stay local.')
            app.wait()
    except KeyboardInterrupt: pass
    finally:stop()

if __name__=='__main__':main()
