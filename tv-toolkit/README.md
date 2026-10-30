# TV Toolkit

Three standalone skills and one coordinator. Install all four directories together to use the coordinator. It locates the sibling skills; it does not embed a second implementation of their procedures.

The workflow is: identify and authorize the right Android TV → record baseline/recovery → establish a working new Home → apply selected privacy/cleanup changes → set up TV-local media → verify playback, physical buttons and reboot → close temporary debugging.

Start with [tv-setup-suite](tv-setup-suite/SKILL.md) for the whole job. Read [discovery and access](tv-setup-suite/references/discovery-and-access.md) for network discovery and pairing. Each individual skill also describes the minimum access it requires.

## What the original session taught us

- IP addresses changed. Model, platform and a private saved identity were more reliable than an old IP.
- SSH was unavailable; authorized Android debugging was for setup, and paired Android TV Remote worked for ordinary control afterward.
- Couchy and an earlier Home redirect produced a Google Home flash; TV Bro was also removed. The final launcher was CleanYourTV, not Couchy.
- Disabling OEM services broadly broke Home, Netflix, YouTube and Settings buttons. Restoring the original key handler fixed them; a key-only launcher helper then preserved shortcuts with the custom Home.
- Google TV setupwraith can intercept Home and own saved Wi-Fi networks. Direct handover worked only after checking that dependency and accepting the remaining tradeoff.
- Lampa's native Android torrent handoff needed `internal_torrclient=false`. An earlier file with `true` was superseded.
- TorrServe needed storage access to persist configuration. Removing it made the earlier successful access-control change unreliable.
- Starting a player was insufficient: playback was verified with the engine initially stopped, buffered video, a playing media session and user-confirmed audio/video.
- A refused ADB port and a reboot request did not prove the final physical debugging switch was off or that a reboot occurred.

The source TV was a low-memory TCL BeyondTV4 / Android 11 device, advertised as 58S470G. This is a reference environment, not a promise that all TCL models behave alike. Vizio OS, Roku, webOS, Tizen and Xumo require a different platform workflow.

## Sources

Historical first-TV artifacts were reconciled against the final setup record, final Lampa config, on-demand playback evidence, package-change records and theme on 2026-10-30. Private source audits, addresses and certificates are intentionally excluded. Release assets and the CleanYourTV source commit were checked against public GitHub metadata when this set was created.

Start each real job with fresh discovery, dependency inspection and source verification. Preserve changes outside the current skill's scope. Never treat these documents as authorization to modify an unrelated TV, contact another person, publish device records or replace firmware.
