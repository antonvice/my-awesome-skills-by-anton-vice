# Privacy and performance procedure

## Baseline and recovery

Record model, manufacturer, device/build, Android SDK, ABI list, RAM, free storage, active user, package states, Home owner, accessibility services, assistant/recognition assignments and relevant settings. `scripts/snapshot.py` collects these without setting or disabling anything. Full dumps may contain private app/media identifiers: keep them outside version control.

Before each mutation record: target identity/user, exact setting/package/component, prior value/state, intended change, result and readback. For app operations record package and UID modes, since a shared UID can affect other apps. Back up supported app exports rather than assuming a production app supports `run-as` or `adb backup`.

For bulk package work, clone [CleanYourTV](https://github.com/Gathin23/cleanyourtv) at a reviewed revision (original `6ffa7fa5df7c38714cd89fd77fe636c53e759083`). Create `tools/venv` with its requirements. Its `tools/privacy.py` reports evidence/candidates; **do not apply its generated list without reviewing dependencies and the owner's choices**.

```bash
# From the CleanYourTV checkout, with TV_HOST set to this session's verified IP:
tools/venv/bin/python -I tools/privacy.py
# After review, write your own small batch under work/; do not start from every package:
tools/disable.sh work/reviewed-batch.txt
# Restore using the same list path and its matching private recovery record:
tools/restore.sh work/reviewed-batch.txt
```

Copy private recovery records from `~/.cleanyourtv/` to the job's private archive. Preserve the list bytes, revision and original absolute path; the original implementation keys records by host and a hash of the list path. DHCP changes and moving the checkout can change the lookup. Follow the reviewed version's recovery implementation to migrate the matching record only after verifying the device; never substitute someone else's snapshot. Launcher installation has its own handover changes, so preserve the pre-install Home/package state separately too.

Package disabled states can be checked with `pm list packages -d --user 0` and package dumps; verify the current user rather than blindly using 0 on a multi-profile TV. `pm disable-user` retains data and system files. `pm uninstall --user` does not provide the same recovery semantics and is not a default system-cleanup strategy.

## Optional sharing, ACR and microphone

Use the firmware's visible Privacy / Usage & Diagnostics / Viewing Data / ACR / Advertising / User Experience settings. On the original TCL, `global tcl_diagnostic_status` and `global tcl_uxp_status` changed from `1` to `0`; these keys are vendor-specific. An arbitrary `settings put` can create a key that no service reads, so require evidence the key already exists and the firmware actually consumes it.

The source TV's Google Usage & Diagnostics switch was changed in the UI. Cast still reported sharing on until a normal reboot. Read its optional endpoint, when available:

```bash
curl --max-time 5 "http://$TV_HOST:8008/setup/eureka_info?options=detail"
```

Inspect only `opt_in.crash`, `stats` and `opencast`; avoid publishing the whole device report. Final source-TV readback was false for all three. A rejected HTTP POST was a failed attempt, not a successful opt-out. Do not invent an unauthenticated mutation API or assume this endpoint exists on every firmware. Google describes [optional and essential Cast data](https://support.google.com/chromecast/answer/6076570?hl=en); disabling optional sharing does not establish no manufacturer communication.

For voice-off cleanup, record `settings get secure assistant`, `voice_interaction_service`, `voice_recognition_service` and the related package/runtime permission/app-op state. Clear those assignments only within the user's desired voice scope. App-level `RECORD_AUDIO ignore` did not always persist on the source firmware; revoked runtime RECORD_AUDIO plus verified effective UID mode survived reboot. Read back effective state rather than relying on a successful command. Do not revoke permissions from unrelated shared-UID services without assessing their effect.

`dumpsys media_projection`, `dumpsys audio` recording monitor and `cmd appops get --user USER PACKAGE RECORD_AUDIO` help distinguish current capture/access history from capabilities. ACR can analyze HDMI imagery without a microphone or Android MediaProjection session. Conversely, a legitimate screen-mirroring session uses capture by design. Avoid both blanket surveillance claims and blanket assurances.

## Performance

Useful observations: `dumpsys cpuinfo`, `cat /proc/meminfo`, `dumpsys meminfo PACKAGE`, `am start -W -n PACKAGE/ACTIVITY`, `df -h /data`. Treat failed/unavailable commands as unknown, not zero. Cold-start timing requires a deliberate force-stop of only the target app; don't disrupt a playing video for a benchmark. Use several comparable runs and report median/range instead of one favorable number.

The reference setup set global `window_animation_scale`, `transition_animation_scale`, and `animator_duration_scale` to `0`. Use `0` or `0.5` according to user preference, recording absent keys distinctly. Disable app boot-start, cloud sync, moving backgrounds and heavy effects where the user doesn't need them. Do not confuse a smaller launcher with a replacement kernel or a guarantee that all video buffering will disappear.

## Debugging closure

Keep authorized ADB available until the Home, network, package rollback and final reboot checks pass. Then disable network/wireless debugging using the device's supported controls, revoke setup authorizations where requested, turn USB debugging off on the TV, and verify from another LAN device. Port refusal is evidence about that listener; timeout/host unreachable is inconclusive. Verify paired Android TV Remote still works and confirm the physical switch/reboot with the user. Never claim a reboot from a command being sent: compare uptime or boot identifiers.
