---
name: tv-lampa-torrserve
description: Install and configure Lampa, a TV-local TorrServe/TorrServer engine and Just Player on Android TV or Google TV, including Russian UI and on-demand playback without a laptop server.
---

# TV-local Lampa and TorrServe

Reproduce the working movie stack: **Lampa → native Android torrent handoff → TorrServe FOSS → TV-local TorrServer → Just Player**. TorrServe/TorrServer is not Tor; do not install a Tor relay or claim anonymity.

## Establish the target

Confirm an Android/Google TV, its current IP, API level, ABI list, RAM/storage and authorized ADB serial. Discover via mDNS `_androidtvremote2._tcp` / `_googlecast._tcp`, ARP and device Settings; do not reuse an old address or run this on Vizio OS/Roku. Enable developer debugging and accept the on-TV authorization. Specify `adb -s "$TV_SERIAL"` in every device command. Android 11 on the source TV was 32-bit ARM despite the chipset; choose the executable ABI the OS actually supports.

Preserve existing app data and record currently installed package versions, user-selected player/search settings, boot preferences and battery exemptions before changing them. Existing source accounts and credentials stay local. This skill does not remove unrelated apps, change Home or modify remote buttons.

## Install and configure

1. Read [the exact recipe](references/recipe.md) and [installer manifest](assets/installers.json). Obtain installers from official releases or F-Droid. The known-good versions are a reference; when updating them, inspect source/API changes and revalidate the playback path. Verify APK identity, signing certificate, version, architecture and SHA-256. Do not replace an existing installation with a different signer by uninstalling its data.
2. Install Lampa `top.rootu.lampa`, TorrServe FOSS `ru.yourok.torrserve`, and Just Player `com.brouken.player`. Install the matching official TorrServer binary through TorrServe's supported local-file installer. Confirm `/echo` reports the intended engine version.
3. Use [lampa-config.json](assets/lampa-config.json), adapted for the user's language and chosen search provider. Generate its Android backup files with `scripts/lampa_backup.py`; import through the app's own Backup/Restore UI. The final value **`internal_torrclient="false"`** enables the native on-demand handoff. Select Android playback and Just Player; disable cloud sync and unnecessary animation/preloading.
4. Configure TorrServer through an ADB forward to its loopback port. `scripts/torrserver_config.py` is read-only by default; `--apply --backup PATH` records original settings/access control and applies the original 64 MiB RAM-cache profile. Read back settings and loopback-only WAF rules. Verify a request from another LAN device receives HTTP 403, then repeat after an engine restart. Do not forward port 8090 through the router.
5. Disable boot auto-start in both app UIs. On TCL, inspect support for the vendor `AUTO_START` app-op before setting it to `ignore`. Do not leave either app battery-exempt as a generic optimization. TorrServe required shared-storage permission on the reference build; revoke Lampa's temporary import storage grant after import. Keep microphone, camera and location denied unless the user needs them.

## Prove the result

- Start with TorrServe **fully stopped**, then open Lampa and select a seeded, authorized test film such as Big Buck Bunny. Do not substitute a direct player launch or a manually prestarted server for this check.
- Verify Lampa opens TorrServe's PlayActivity, which starts the local engine and hands video to Just Player. In `dumpsys media_session`, playing is `state=3`, speed `1.0`, buffering ahead and no error. Ask the user to confirm visible picture, audible sound and any required Russian track/subtitles.
- Return Home, reboot normally and prove that reboot occurred using uptime/boot evidence. Check boot auto-start remains off, then repeat the on-demand path and local-control rejection. No laptop-hosted server may be required.
- Restore the intended TV foreground, remove only this job's temporary shared-storage files and ADB forward, and close temporary debugging if no further setup needs it. Report any pending physical confirmation.

Russian UI does not guarantee Russian audio; release metadata and track selection determine it. Search queries leave the TV for the selected provider. The historical provider is not a trust endorsement or a permanent availability guarantee. Torrent streaming still contacts peers; the upload-disable flag does not establish anonymity or zero protocol traffic.

## Recovery

Keep pre-existing app versions/configuration and server settings/WAF backups private. Revert through the app UI or the version-matched server API; restore the prior boot preference, grants and player choice rather than enabling everything. Remove newly added apps only if requested. A failed source search is distinct from a broken player/server; isolate metadata lookup, peer access and player handoff before reinstalling anything.
