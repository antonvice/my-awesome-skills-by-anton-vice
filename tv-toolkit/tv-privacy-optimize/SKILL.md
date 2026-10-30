---
name: tv-privacy-optimize
description: Audit and reversibly optimize Android TV or Google TV by reducing unwanted apps, optional analytics, ACR and voice access while preserving chosen apps, playback, input switching, updates and remote controls.
---

# TV privacy and performance

Make measured, reversible changes to the identified TV. Keep the owner's current apps and functions by default; do not copy another person's entertainment-app allowlist or chase a target count of disabled packages.

## Inspect first

Discover the current address with mDNS/ARP/SSDP, verify Android/Google TV model and firmware, then obtain on-TV debugging authorization. Pin every command with `adb -s "$TV_SERIAL"`. Non-Android Vizio/Roku/webOS/Tizen are outside this procedure. Use `scripts/snapshot.py --serial "$TV_SERIAL" --out private/before` for a read-only inventory. Store device identities, logs, dumps and recovery records privately. The script is a baseline, **not a complete rollback**; record each changed setting, grant, app-op and package state before mutation.

Agree on the functions to preserve using available context: installed apps, accounts, DRM playback, casting/AirPlay, Settings, Wi-Fi, Bluetooth, TV/HDMI, remote buttons, updates and any desired voice control. Ordinary cleanup authorization covers reversible changes within that scope. Ask only where a material dependency tradeoff remains unresolved.

## Apply the smallest useful changes

1. Read [privacy and optimization procedure](references/procedure.md). Inspect package manifests/services, app-op history and firmware settings. Distinguish evidenced telemetry/ACR from names that merely look suspicious. Do not describe CAMERA permission, a process name or a blank activity dump as proof that the TV takes secret screenshots.
2. Disable optional Usage & Diagnostics, vendor viewing-data/ACR, personalization/advertising and diagnostic opt-ins through supported settings. Save the previous values and read them back. Check Cast's own opt-in report after reboot rather than assuming the UI switch propagated immediately.
3. Use a reviewed, device-specific list with CleanYourTV's snapshot-backed disable/restore tools or equivalent recorded `pm disable-user --user USER` operations. [TCL examples](references/tcl-reference.md) identify historical candidates and the dependencies that broke remote control. Keep system partitions, core providers, input handlers, network stack, DRM, WebView, package installer and updater intact. Disable a few justified packages at a time, verifying before continuing. Uninstall an ordinary app only when that removal is in scope and its account/data consequences are understood.
4. If the owner wants voice off, clear selected voice services and revoke unnecessary microphone grants/app-ops, recording original values. Inspect shared UID implications and effective modes. Keep needed mirroring permissions. Do not disable a remote-service package merely because it has a microphone permission; ordinary paired remote control and voice audio are different capabilities.
5. Reduce animation scales and app background work where useful. Keep changes reversible; do not alter CPU governors, memory-killer tuning, swap or security services. Avoid indiscriminate cache/data wipes, force-stop loops and memory cleaners. RAM used for cache is not automatically wasted RAM.

## Verify behavior and claims

Measure comparable idle CPU, available memory, launcher PSS and repeated cold/warm launch timings before/after with the same apps, idle interval and network conditions. Individual snapshots do not establish a controlled speedup. Attribute changes separately from a reboot.

Test Home, Back, Settings, Netflix/other chosen shortcut apps, YouTube/its chosen replacement, Input, volume tap/hold, Bluetooth and any required voice/mirroring path. Launch and play retained DRM video, not just its splash screen. If a button breaks after a batch, restore that batch and isolate the key handler instead of disabling more packages.

Reboot normally, verify uptime changed, then re-check privacy values, effective microphone permissions/app-ops, enabled packages, startup activity, Wi-Fi and physical remote behavior. `dumpsys media_projection`, audio recording monitor and app-ops provide observations at a point in time; they do not certify all proprietary firmware or zero outbound traffic. Only claim reduced traffic if measured with an appropriate capture and attribution. Do not claim universal ad blocking; Home ads and YouTube ads have different sources.

Restore the intended screen and close temporary debugging once remaining setup is complete. Confirm the TV's physical debugging switch/revocation and test paired remote control after closure. A refused TCP port alone does not prove the USB setting is off.

## Recovery and report

Reverse only this job's successful changes, in reverse order, to their recorded original states. A package originally disabled remains disabled. Restore an absent setting using `settings delete`, not the literal string `null`. Restore a user-disabled package's exact enabled/default state instead of blanket `pm enable`. Revert permissions/app-ops only to observed prior values; some UI consents need manual restoration. Explain what changed, preserved functions, measured results, tradeoffs, recovery location and pending user tests.
