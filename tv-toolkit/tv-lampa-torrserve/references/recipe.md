# Exact working recipe

Reference: Android 11, 32-bit ARM, about 2 GB RAM. The server runs on the TV. Versions and checksums are in `../assets/installers.json`; newer systems may need different ABIs or permission handling.

## Installers and engine

Use `adb -s "$TV_SERIAL" install -r FILE.apk` after checking `aapt dump badging` and `apksigner verify --print-certs`. An install command's process exit status alone is insufficient: require its actual `Success` response and verify the installed package/version. Preserve installed data/signers.

The F-Droid client is version 143, while the downloaded engine is **MatriX.147.1**. These are different components, not a version mismatch to fix. Use F-Droid's FOSS client rather than substituting the differently signed upstream client build. Select the appropriate official `TorrServer-android-*` asset using `ro.product.cpu.abilist`, not the host Mac's architecture.

For the reference build, push `TorrServer-android-arm7` to `/sdcard/Download/`, open TorrServe, choose its local server installation option, and select the file in the TV's picker. Do not assume shell access to the app's private directory. Grant TorrServe READ_EXTERNAL_STORAGE and WRITE_EXTERNAL_STORAGE when supported/needed; it failed to persist settings after those were revoked. Android 13+ may have a different storage model: use the supported picker/UI rather than forcing obsolete grants.

## Lampa settings import

```bash
python3 scripts/lampa_backup.py --config assets/lampa-config.json --out private/lampa-import
adb -s "$TV_SERIAL" shell mkdir -p /sdcard/Documents/LAMPA
adb -s "$TV_SERIAL" push private/lampa-import/settings.backup /sdcard/Documents/LAMPA/settings.backup
adb -s "$TV_SERIAL" push private/lampa-import/storage.backup /sdcard/Documents/LAMPA/storage.backup
adb -s "$TV_SERIAL" shell am start -n top.rootu.lampa/.MainActivity --es cmd open_settings
```

Commands above are relative to this skill folder. Temporarily grant Lampa shared-storage access if the installed version requires it for import. In Lampa's Android settings use **Backup and restore** (`Резервирование и восстановление`) and the applicable restore actions for Android settings and Lampa settings (`Восстановить настройки Lampa`). Inspect the visible UI; do not assume labels or coordinates are stable. Reopen settings to read back the frontend, Russian language, sync-off and player choices. Export through the supported UI if necessary to verify storage values.

`settings.backup` is Android SharedPreferences XML with strings and typed booleans; `storage.backup` stores the frontend values as strings. Do not convert the string `"false"` in frontend storage into an XML boolean. The saved **final** config has `internal_torrclient="false"` and `torrserver_preload="false"`; an earlier successful settings import still contained `true` and was replaced before the actual on-demand test passed.

The original frontend was `https://yumata.github.io/lampa/` and search endpoint `https://jr.maxvol.pro`. The latter is a third-party public provider; verify it is still appropriate/reachable and obtain the user's source preference. If it fails, configure another user-chosen provider without claiming the movie stack is broken or silently adding plugins. The app can be tested with authorized media separately. No paid cloud account was needed.

## Local engine configuration

```bash
adb -s "$TV_SERIAL" forward tcp:18090 tcp:8090
python3 scripts/torrserver_config.py --port 18090
# Once the displayed diff is within scope:
python3 scripts/torrserver_config.py --port 18090 --apply --backup private/torrserver-before.json
```

The helper checks engine version `MatriX.147.1` (override only after inspecting the target version). It merges selected fields into the current `/settings` payload, rather than replacing unknown fields, and posts WAF allowlist `127.0.0.1\n::1`. The HTTP server may still bind broadly; WAF HTTP 403 is the verified access boundary, not proof of a loopback-only socket.

Profile: CacheSize 67,108,864 bytes, PreloadCache 12, ConnectionsLimit 20, timeout 30 s, no disk cache, debug, DLNA, Bonjour, local peer discovery, built-in catalogue search or UPnP; upload disabled. Remaining engine defaults are preserved. A large film can still overrun weak TV hardware: prefer seeded 720p/1080p H.264 on this class of device.

Check from the computer: `curl --max-time 5 -i "http://$TV_HOST:8090/echo"` must return **403** while the same request through the ADB forward succeeds. A timeout is inconclusive, and a forward to a different device proves nothing. In TorrServe's **Choose Player**, select Just Player and save it. Disable boot-start in both apps. The source TV exposed TCL `AUTO_START`; other vendors may not support it, and Android denied changes to individual third-party components. Do not suppress failures and call those components disabled.

After a genuine reboot, check WAF/settings survived and no engine started at boot; then open Lampa and start an authorized test film with the engine initially absent. Inspect `ps -A`, foreground activity and `dumpsys media_session`, then obtain actual picture/sound confirmation. Home and volume must continue working during playback. Do not keep a trial battery exemption unless a verified problem requires it and the owner accepts it.

## Cleanup and rollback

Remove the ADB forward with `adb -s "$TV_SERIAL" forward --remove tcp:18090` and remove only files staged by this job from `/sdcard/Download/` and `/sdcard/Documents/LAMPA/`. Preserve user exports/media already there.

Before restoring the helper's backup, re-check the device identity and current state. Through the same protected tunnel, POST `/settings` with `{"action":"set","sets":<backup.settings>}` and POST `/waf` with the backed-up `whitelist`, `blacklist` and `referers` fields. A backup might reopen LAN control; explain that consequence when relevant. Read back both. Rollback boot settings and app permissions separately; the server backup does not contain them.
