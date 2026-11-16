# German Eiland Overlay — Linux compatibility prototype

**Unofficial, experimental companion scripts for the official German Eiland Overlay.**
Developed during one Fedora KDE / Wayland + Xwayland troubleshooting session with The Isle Evrima. This is a starting point for the server owner and Linux users to review, not an official Linux release or a promise of compatibility.

[Português](README.pt-BR.md) · [Privacy and technical limitations](docs/PRIVACY-AND-LIMITATIONS.md)

## What it does

- Starts a separately obtained, official overlay using an existing Proton Experimental installation and a **new, dedicated compatibility prefix**.
- Uses the overlay's Chromium debugging interface on `127.0.0.1:9340` to read UI frames and settings. An XShape mask removes the otherwise opaque black background and follows newly opened panels.
- Makes the overlay a KWin critical-notification window so it can remain above the focused fullscreen game. This is a window-stacking workaround, not a change to the game's renderer.
- Registers the overlay's configured keyboard shortcuts through KDE KGlobalAccel **only while The Isle has focus**, releasing registrations when focus changes or key rebinding starts.
- Respects the combat/click-through lock. F7 is the default toggle: lock while playing; unlock to click overlay controls.
- Removes problematic panel shadows and replaces the shop species selector with an in-page list. It preserves the site's original select element and dispatches its normal change event; it does not purchase anything.

## What is included

Only source scripts, documentation, and a license for these scripts. **No official overlay executable, game files, Wine/Proton binaries, user profile, Steam login, cookies, screenshots, account data, or session logs are included.**

## Requirements

- Linux desktop running **KDE Plasma / KWin**, a desktop D-Bus session, and X11/Xwayland (`DISPLAY`). Other compositors and native Wine Wayland are not supported by this prototype.
- Steam's existing **Proton Experimental**, installed by the user. The game keeps its existing Steam launch configuration.
- The official German Eiland Overlay, obtained from the server's official download. Keep the **entire installed application folder**, including `resources`, beside the executable. This project does not download it for you.
- Python 3 with Pillow, websockets (including its synchronous client), dbus-python, PyGObject/GLib, and PySide6/QtGui. Also `xprop`, `libX11.so.6`, and `libXext.so.6`.

Use your distribution's packages for desktop-integration libraries. `requirements.txt` names Python dependencies; it is not a guarantee that pip can build every desktop dependency on every distribution.

## Usage

After downloading, run `chmod +x launch.sh` once if the executable bit was not preserved.

```bash
./launch.sh --check
./launch.sh --exe "/absolute/path/to/German Eiland Overlay.exe"
```

If Proton is in a different Steam library:

```bash
./launch.sh --exe "/absolute/path/to/German Eiland Overlay.exe" \
  --proton "/absolute/path/to/Proton - Experimental/proton"
```

Optional: save those paths **locally** and add an application-menu shortcut:

```bash
./launch.sh --exe "/absolute/path/to/German Eiland Overlay.exe" --install-shortcut
```

Keep this source folder in place after creating the shortcut. Start the game normally through Steam. Sign in yourself inside the newly created overlay profile; no account information is supplied by this repository.

The launcher uses these separate user-local locations (respecting XDG directories):

- `~/.config/german-eiland-overlay-linux/config.json`: paths you save with `--install-shortcut`.
- `~/.local/share/german-eiland-overlay-linux/compatdata`: private Wine/Proton profile, including any login created later.
- `~/.local/state/german-eiland-overlay-linux`: helper lock files and local troubleshooting log.

**Never upload those directories.** A port already in use makes this launcher stop rather than attach to an unknown process. You can choose another loopback port with `--port`.

## Controls

The helpers read the overlay's current keyboard bindings, so changed bindings can be reflected while it runs. Default examples from the tested session:

| Key | Action |
| --- | --- |
| F6 | Hide/show overlay |
| F7 | Combat lock: pass mouse clicks to the game / allow overlay interaction |
| F8 | Hold to talk — press/release forwarding is implemented; audio transmission is not validated by this package |
| F9 | Mute microphone |
| 5 | Show/hide menu bar |
| Ctrl+S | Lock/unlock overlay layout |

When interacting, release the game's cursor first, then unlock the overlay if necessary. Re-enable combat lock before fighting. Conflicting KDE shortcuts are reported, not stolen. Mouse-button bindings are **not** implemented by the KDE keyboard bridge.

## Validation status

The original local troubleshooting setup showed the overlay above the live game, a visible game background, clickable panels, and F7 working according to the user. Microphone permission and opening a local capture track were checked, but end-to-end voice transmission was not confirmed. Shop-list scrolling and later fullscreen/edge fixes did not receive a complete final regression check.

The **portable launcher and fresh-prefix distribution flow are newly prepared**. They have dependency/syntax checks, not an independent clean-machine playthrough. The successful local session used overlay 0.5.133 / Electron 42.10.1 and Proton Experimental; later versions may change the private UI internals this prototype relies on.

No server-owner approval or anti-cheat compatibility guarantee has been established. Review with the server owner before recommending wider use. Do not interpret a successful local session as proof that a setup is approved by the server.

## Removal

Stop this launcher and close the overlay. Remove its application-menu shortcut, if you created one:

```bash
rm -- "$HOME/.local/share/applications/german-eiland-overlay-linux.desktop"
```

Then remove this downloaded source folder when no longer needed. Your private profile, saved paths, and logs remain in the user-local directories listed above; back up anything you want before manually removing them. The launcher does not change Steam game options or install a persistent KWin rule. Window type and XShape changes end with the overlay window.

## For the server owner

The useful parts to review are `src/window-bridge.py` (window visibility and input), `src/shortcut-bridge.py` (KDE keys), and `src/shop-select-fix.js` (native-select workaround). All are external companion scripts. No proprietary app archive is patched or redistributed. A future native Linux build or documented overlay API would be preferable to depending on Chromium debugging and private JavaScript names.

## License

MIT for this repository's companion scripts only. German Eiland Overlay, The Isle, Steam, Proton, and dependencies retain their own licenses and ownership. Names identify compatibility targets; no affiliation or endorsement is implied.
