# Cyberpunk theme

The included wallpaper is the actual static neon city artwork used in the final setup, with dark navy, cyan/magenta lights, a quiet clock area and a dark lower dock region. No image generation service is needed to reuse it. Its prompt is included beside the image if the owner requests a new composition.

`assets/cyberpunk/config.json` reproduces the original low-memory layout:

- Four columns, single row, halo glass dock, opacity 70, wallpaper dim 18.
- Background `#050916`, true-color wallpaper, icon-only controls, clock/date.
- App library, tile menu and launcher settings button enabled.
- Animations, advanced effects, ambient/app glow, overshoot, fading and module cards off; reduced motion on.
- Historical dock Netflix, SmartTube, Lampa and AirPlay; BrowseHere remained available in Apps. Substitute the actual owner's chosen apps. An app absent from the dock is not a request to uninstall it.

Start with a copy of the included theme in a private work directory. Review `dock_apps`, `hidden_apps`, `live_tv_package`, `restore_key_services`, and especially `app_keys` against the current TV. Remove unknown scan-code mappings before applying the theme to another remote. Hidden apps are a presentation choice, not proof that they are disabled.

From the CleanYourTV checkout:

```bash
# TV_HOST is this session's verified address; use an absolute path to your adapted theme.
tools/theme.sh /absolute/path/to/private/cyberpunk
```

The supported theme importer handles protected Android/data storage and content-provider ownership. A direct shell copy can appear successful while the app cannot read the resulting file. Verify the theme's applied configuration through its supported provider/export, compare the bytes/checksum where possible, and inspect Home with the user. Theme push resets relevant on-TV overrides; keep the prior theme and user choices for rollback. `tools/theme.sh --reset` returns to built-in defaults, **not necessarily the user's previous theme**.

For a faster theme, keep wallpaper static and disable live/video wallpapers, overlays and unused module cards. For more motion, turn on one supported option at a time and recheck focus movement, held keys and memory. Styling stock Google TV windows is not what this launcher does: Android system dialogs and apps keep their own UI.
