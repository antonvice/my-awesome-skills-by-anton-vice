# Home handover and physical keys

## Build and preserve recovery

```bash
git clone https://github.com/Gathin23/cleanyourtv.git
cd cleanyourtv
git checkout --detach 6ffa7fa5df7c38714cd89fd77fe636c53e759083
python3 -m venv tools/venv
tools/venv/bin/pip install -r tools/requirements.txt
```

Set `TV_HOST` to the freshly verified device IP. Read `launcher/build-and-install.sh`, `tools/disable.sh`, `tools/recovery.py`, manifests and current docs. Test/build with the upstream commands and Android SDK/JDK they require. The original build passed 274 tests and lint; that is historical evidence, not a test result for a future checkout.

Before installing, record `cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME`, each relevant package enabled/default state, `settings get secure enabled_accessibility_services` and `accessibility_enabled`. Save the original stock component explicitly; resolving it later after disabling packages may return a fallback instead. Pre-existing accessibility services and grants must survive both installation and rollback.

The installer can disable recognized stock launchers and grant location; it does more than copy an APK. Use `STOCK_LAUNCHER=none launcher/build-and-install.sh` for a staged first install where needed; inspect that script's actual behavior because it still attempts to set Home and may report failed handover. Build/install and `am start -W -n com.gathin.tvhome/.MainActivity` separately when staged installation is necessary. Do not ignore a handover failure just because the APK installed.

## setupwraith and Google Home flicker

On some Google TVs, `com.google.android.tungsten.setupwraith/.RecoveryActivity` answers HOME with higher priority even after CleanYourTV holds the Home role. A redirect from stock Home caused a visible Google flash on the reference TV. Direct handover disabled the stock launcher **and** setupwraith, but setupwraith can own saved networks.

Inspect private `dumpsys wifi` ownership (`cname=`) for the current and other saved networks before disabling setupwraith. Don't publish SSIDs/password-related dumps. If the current network belongs to setupwraith, keep it enabled and reconnect the network through Settings so ownership can migrate, using the local physical remote/password. Re-check ownership. If moving saved networks could remove profiles or affect casting, explain that concrete tradeoff and use existing authorization or obtain the owner's decision. The source user explicitly accepted possible loss of another saved Wi-Fi profile; that approval does not transfer to future users.

Use upstream safety checks; do not set `FORCE_SETUPWRAITH`, `FORCE_HOME`, `TVINPUT_ALLOW` or `HANDLERS_ALLOW` to conceal a failed dependency check. Keep working stock Home until the new activity works and the setup conflict is resolved. For a direct handover, use a device-reviewed list with the affected setup package and preserve a pre-change recovery record. A future device may require retaining its factory Home: explain that limitation rather than claiming a complete replacement or silently using a flickering redirect.

Expected final Home: `com.gathin.tvhome/.MainActivity`. Verify with the resolver, foreground activity and repeated **physical** Home presses, not just an injected launch. TV/HDMI and native Settings must still be usable.

## Key-only helper and mappings

Source firmware routed some app/gear/input keys through OEM services. Broad removal broke them; restoring the original handler fixed all four tested keys before remapping. Preserve those services and use the launcher's helper for only the missing mappings.

The reviewed installer supports `HOME_KEY_SERVICE=1`, `INPUT_KEY_SERVICE=1` and `RESTORE_KEY_SERVICES=1`. The source setup used **HomeKeyService** for its app/gear/remote mappings; InputKeyService is conditional, not something to enable blindly alongside it. RESTORE_KEY_SERVICES grants WRITE_SECURE_SETTINGS so helpers can be repaired after force-stop/reinstall. Explain and record that optional persistent grant. Verify the service requests key filtering but not window-content retrieval and preserves existing enabled services. Reinstallation can unbind a helper even while its name stays listed; inspect bound services after install, theme restart and reboot.

Reference remote `BT_RC813_M1` mappings:

| Physical key | Example theme entry |
| --- | --- |
| Netflix | `scan:242:com.netflix.ninja` |
| YouTube | `scan:245:org.smarttube.stable` |
| Gear/Settings | `scan:233:settings` |
| Branded TCL HOME (not house Home) | `scan:204:top.rootu.lampa` |

For another remote, inspect `getevent -lp`, then capture a short `getevent -lt /dev/input/eventN` while the user presses the specific key. Stop capture promptly. The source TCL HOME key emitted EV_KEY `00cc` (decimal 204), matching `TCL_DASHBOARD` in its key layout. Do not confuse EV_KEY values, Android keycodes and scan codes, or remap the house-shaped Home to Lampa. If input-event access is denied, use upstream key diagnostics or a supported remapper instead of trying privileged exploits.

## Rollback

Re-enable only packages that this job disabled, preserving each original default/enabled state; restore the recorded stock Home component after its package is available. Use the matching upstream list/recovery record for list changes and explicitly restore installer changes not covered by it. Restore the previous accessibility list/state without deleting services added independently later; remove only this launcher's helper entries and revoke only grants newly added by this job. Restore original app-ops and location permission as recorded. Do not blindly enable every package or overwrite another session's recovery file. Saved Wi-Fi profiles removed by disabling setupwraith may need manual rejoining.
