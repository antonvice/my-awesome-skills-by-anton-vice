---
name: tv-setup-suite
description: Coordinate Wi-Fi discovery, authorized Android TV access, reversible privacy/performance cleanup, a cyberpunk CleanYourTV launcher, and TV-local Lampa/TorrServe playback as one verified setup.
---

# Complete TV setup

Coordinate the three companion skills. The owner chooses apps and functions; do not reduce their TV to the original example's four apps. This is a launcher/configuration/media setup, not a root exploit or replacement firmware.

## Discover and establish access

Read [discovery and access](references/discovery-and-access.md). Find the TV on the current LAN, confirm manufacturer/model/platform, pair normal remote control and obtain physical ADB authorization for setup. Identify the exact target when multiple TVs are present. Stop the Android procedure on Vizio OS, Roku, Tizen, webOS or Xumo; explain the platform boundary rather than deploying Android packages to it.

The generic `scripts/remote.py` uses paired Android TV Remote v2 for regular controls and needs no open ADB listener. Require `--host` and a private per-device `--state-dir`; it intentionally has no hard-coded IP/MAC, certs or background daemon. App launch URIs and foreground reports are checks to combine with visible behavior, not proof of playback.

## Sequence the work

Locate the sibling `tv-privacy-optimize`, `tv-cleanyourtv-launcher` and `tv-lampa-torrserve` skills beside this one (or through the host skill registry). If a companion is missing, explain the missing dependency; do not pretend the coordinator contains its full procedure.

1. Load **tv-privacy-optimize** for its baseline and dependency review. Save private identity, exact original states and recovery files. Establish which functions matter from the user's request/context, asking only about unresolved consequential choices. Do not apply a stock-launcher removal as generic cleanup.
2. Load **tv-cleanyourtv-launcher**. Install/launch the new Home first; resolve setupwraith/Wi-Fi ownership, enable only the needed key helper, and apply an adapted cyberpunk theme. Test physical Home and native Settings before disabling optional packages.
3. Complete the reviewed **tv-privacy-optimize** changes in small batches while checking retained apps, remote keys, Wi-Fi, DRM, casting and HDMI. Keep a private change ledger, not just a list of successful shell exits.
4. Load **tv-lampa-torrserve**. Install the TV-local, on-demand stack. Keep its server loopback-controlled and preserve the native handoff. Verify actual authorized movie playback with the server initially stopped.
5. Add other requested apps independently from their official sources, preserving user data and signing identity. SmartTube is optional for YouTube without its normal ad playback; BrowseHere, Netflix and mirroring are choices, not mandatory removals or installs. App-level ads elsewhere are not solved by changing Home. Do not add search plugins/providers, accounts or browser-site testing beyond the user's scope.
6. Run the acceptance checks below; then close setup debugging and retain the paired remote and private recovery instructions.

## Acceptance

- Repeated physical Home opens the chosen launcher directly; no Google Home flash, setup loop or dead end. Library/native Settings and all retained apps remain reachable.
- Home, Back, branded app shortcuts, Settings, Input and volume tap/hold work. Verify any custom branded button mapping separately. ADB key injection is not the physical-button test.
- Chosen DRM streaming and Lampa playback show video and audio. The Lampa path works with the engine initially stopped and without the laptop serving files. Its control endpoint rejects LAN access after engine restart.
- If mirroring is in scope, test from each required Mac/iPhone/iPad with picture **and** sound. Discovery alone is insufficient. Prefer the existing working receiver; do not replace it simply because the original TV used another one. Keep on-demand receivers PIN protected and verify listener shutdown after exit where supported.
- Before/after performance measurements use comparable conditions; distinguish observed change from a promised speedup. Record exact privacy opt-ins/effective grants and limitations of closed firmware.
- A normal reboot is verified from uptime or boot evidence, and Home, helper binding, Wi-Fi, package states, privacy and on-demand movie playback survive it.
- Close wireless/network and USB debugging using supported controls. Verify the physical switch/authorization state and paired remote afterward. Report unreachable hosts, inconclusive ports and pending physical tests as pending.

If a required check fails, isolate and reverse the last relevant change before expanding the cleanup. Keep a functioning Home and recovery path throughout. End with a concise inventory of changes, measured/confirmed results, unresolved checks and local recovery paths. Do not publish raw device records or leave temporary local servers/forwards running.
