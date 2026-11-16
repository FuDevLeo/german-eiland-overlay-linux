# Installation guide — Fedora KDE

[Project overview](../README.md) · [Guia completo em português](INSTALACAO.pt-BR.md)

## First: installation is not execution

The original setup used **standalone Wine to run the official Windows installer**, then **Proton Experimental to run the installed overlay**. Proton contains a Wine-derived runtime, but installing the whole application using only Proton has not been validated here. This documented route therefore requires Wine **and** Proton at different steps.

The distribution launcher expects `German Eiland Overlay.exe` and its full installed application directory. It does not run the `...Setup...exe` or install the app for you.

This is an unofficial prototype, not a clean-machine installation certified by the server owner. Review the [validation limits](PRIVACY-AND-LIMITATIONS.md) before starting.

## 1. Prepare the desktop and tools

Use KDE Plasma/KWin with a desktop D-Bus session and X11/Xwayland. The Isle should already work through Steam. Install **Proton Experimental** from Steam's Library/tools; do not change the game's Proton selection for this guide.

The launcher looks for native Steam at `~/.local/share/Steam` or `~/.steam/steam`. Steam Flatpak, other sandboxes, non-KDE compositors, and native Wine Wayland have not been validated.

On Fedora, these package names correspond to the components present during troubleshooting:

```bash
sudo dnf install wine git python3-pillow python3-websockets python3-dbus \
  python3-gobject-base python3-pyside6 xprop libX11 libXext
```

Review the proposed transaction before confirming, especially unexpected removals. Package availability varies by Fedora release. Use distribution equivalents elsewhere. No SELinux changes, signature bypass or reboot are required by this prototype. System Python is the simplest way to keep desktop libraries (`dbus`, `gi`, PySide6) available.

## 2. Install the official overlay with Wine

Obtain the setup executable from the official **[German Eiland](https://germaneiland.com/)** channels. This repository does not redistribute it.

Choose a dedicated installation prefix:

```bash
GE_INSTALL_PREFIX="$HOME/.local/share/german-eiland-overlay-linux/installer-prefix"
mkdir -p "$GE_INSTALL_PREFIX"
WINEPREFIX="$GE_INSTALL_PREFIX" wine "/actual/path/to/the/official-setup.exe"
```

Replace the quoted installer path with your actual file. Follow the official installer. Disable its option to launch immediately, if offered: the normal launch will use this project's Proton launcher. If the app opens under Wine and stays white, close that overlay instance normally; do not kill all Wine processes or the game.

Keep the **entire installed folder**, including `resources` and adjacent libraries. Locate its executable with:

```bash
find "$GE_INSTALL_PREFIX/drive_c/users" -type f -name 'German Eiland Overlay.exe'
```

A typical location is `drive_c/users/YOUR_USER/AppData/Local/Programs/German Eiland Overlay/German Eiland Overlay.exe` inside the installation prefix. `YOUR_USER` is a placeholder. Use the installed application executable, not the setup executable.

You can also use an existing official app installation on your own machine. Never share its full Wine profile with another user.

## 3. Download and check this project

```bash
git clone https://github.com/FuDevLeo/german-eiland-overlay-linux.git
cd german-eiland-overlay-linux
chmod +x launch.sh
./launch.sh --check
```

Alternatively, use GitHub's **Code → Download ZIP**, extract it, and open a terminal in the directory containing `launch.sh`. Then run the last two commands above.

The dependency check does not start the game or prove that interactive behavior works.

## 4. Run the installed overlay with Proton

```bash
./launch.sh --exe "/full/path/to/German Eiland Overlay.exe"
```

For a different Steam library:

```bash
./launch.sh --exe "/full/path/to/German Eiland Overlay.exe" \
  --proton "/full/path/to/Proton - Experimental/proton"
```

The `--proton` path must end in the `proton` script, not in a directory or Wine executable.

The launcher creates a **new runtime profile** at `~/.local/share/german-eiland-overlay-linux/compatdata`. It does not copy the Wine installer prefix, Steam game prefix, cookies or accounts. The installed application remains at the original path, which must stay available. Sign in yourself in this new runtime profile, and start The Isle normally through Steam.

The original local setup worked with this separation of tools. The portable launcher/fresh-profile flow still needs an independent end-to-end test.

## 5. Add the correct shortcut

```bash
./launch.sh --exe "/full/path/to/German Eiland Overlay.exe" --install-shortcut
```

Include `--proton` if you needed it previously. This saves paths locally and creates **German Eiland Overlay (Linux prototype)** in the application menu; it does not start anything. Keep the source directory in place, or recreate the shortcut after moving it.

The shortcut produced by the Wine installer may launch the unadjusted Wine app. Use this project's shortcut for the compatibility helpers.

## 6. Controls and troubleshooting

Defaults: **F6** hides/shows; **F7** toggles combat/click-through lock; **F8** is hold-to-talk; **F9** mutes; **5** toggles the menu bar; **Ctrl+S** locks layout. The helpers follow the overlay's current bindings and register keyboard shortcuts only while The Isle has focus. Conflicting KDE keys are not stolen; mouse-button bindings are not implemented.

Keep combat lock on while playing. To interact, first release the game's cursor and unlock the overlay with F7. Re-enable it before combat. **Esc** cancels a key capture; rebind one row at a time. Microphone and voice communication were confirmed working by the user in the original Fedora KDE installation; the portable package still needs testing on another machine.

| Problem | Check |
| --- | --- |
| White window | Use the project's Proton shortcut, not the installer's Wine shortcut. |
| Black background or cut panels | Check dependencies/helpers. XShape is a binary cutout, not true alpha blending; dark content and edges can be imperfect. |
| Cannot click | Check F7 and whether the game has released the pointer. |
| Hotkeys fail in game | Check KDE, key conflicts, game focus and the game's X11 window class. |
| Port is already in use | Close the previous overlay or choose `--port 9341`; do not kill the game or expose the port to the network. |
| Shop species menu is hidden | The helper replaces it with an in-page list. Site updates may require a new fix. Scrolling still needs complete regression testing. |
| Microphone issues | Microphone and voice communication worked in the original installation. Check the local input device and app permission if your setup differs. |
| Desktop panel appears at the screen edge | The user reported this resolved by using fullscreen with the overlay window-stacking workaround. Other installations still need testing. |

## Private files and removal

The installer prefix, runtime `compatdata`, `~/.config/german-eiland-overlay-linux/config.json`, and `~/.local/state/german-eiland-overlay-linux` are **private local data**, not files to upload. They can contain login sessions, paths and logs. Review/redact any log before sharing. Default locations follow XDG variables when set.

Chromium debugging is loopback-only but can control an authenticated app session. Do not forward/expose that port. See [privacy details](PRIVACY-AND-LIMITATIONS.md).

Close the overlay/launcher, then remove `~/.local/share/applications/german-eiland-overlay-linux.desktop` if installed and remove this downloaded source directory when no longer needed. Profiles and logs are retained; remove them manually only after backing up anything you want. No Steam game settings or game files need to be modified for this procedure.
