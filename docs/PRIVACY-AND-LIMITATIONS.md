# Privacy, implementation boundaries, and known limitations

## Publication boundary

This repository was prepared from an explicit source-file allowlist. It does not import a user's Wine prefix, browser profile, Steam data, logs, game configuration, screenshots, conversations, local Git history, or proprietary app archive. Configuration paths are generated on each user's own machine and are not source files.

## Runtime access

The prototype enables Chromium's debugging interface on loopback, then attaches only to the overlay UI (`ovl3://overlay/index.html`) and, for the selector workaround, the official shop (`https://germaneiland.com/shop/`). The helper can read and manipulate those pages while running. That includes an authenticated overlay/shop session if the user logs in.

The window helper captures the **overlay's rendered frame**, in memory, to calculate a visible-window mask; it does not write these frames to disk. The shortcuts helper reads configured hotkeys and overlay interaction state. It does not implement general key logging. Locally registered shortcut action names and errors can appear in the launcher log. Audio capture, translation, game-memory reading, game-process injection, account transfer, purchasing, and automatic chat sending are not implemented by these companion scripts.

The F8 bridge forwards the user's push-to-talk press/release to the official app. Actual microphone processing and voice connections remain functions of the official app. This repository does not record or upload audio.

**Loopback debugging is powerful.** Other local processes may be able to control the logged-in application through that port. Never bind it to a public interface, forward it through SSH, expose it to a LAN, or publish session logs/profiles. Closing the overlay closes its endpoint. The repository includes no remote telemetry or analytics service.

## Rendering and input

- XShape is a binary region: it cannot reproduce true translucent blending. Very dark UI content can be removed or have rough edges.
- A screenshot/mask refresh runs about twice a second. Menus may take a moment to appear, and there is CPU/X-server overhead. Test performance on your own hardware.
- The scripts depend on private UI names such as `S`, `HK`, `N.ui`, and `VOICE`. An overlay update can break them.
- A critical-notification window type places the overlay above fullscreen windows. This is a KWin workaround, not an officially supported overlay mode. Its interaction with other fullscreen applications, focus changes, and accessibility tools needs wider testing.
- Keyboard shortcuts are active only when the X11 window class identifies The Isle (`steam_app_376210`). Native Wayland game windows, other compositors, mouse-button bindings, and some Steam sandbox arrangements may not work.
- Key rebinding temporarily releases KDE registrations after the next polling cycle. There can be a short transition delay.
- The shop fix changes only the species selector's presentation and invokes the original selection/change behavior. Its newest scrolling fix has not had a complete interactive regression test.

## Validation limits and cooperation

One local session is evidence that the approach can work; it is not certification of the portable package, a server-policy decision, or proof of anti-cheat safety. The server owner's permission to distribute or recommend this integration has not been established. Ask the owner to review the approach and preferably provide a supported API or native Linux build.

When reporting a bug, describe the desktop session, overlay version, Proton version, steps, and visible result. Review/redact logs yourself before sharing; do not send cookies, Steam identifiers, private profiles, or a full troubleshooting directory.
