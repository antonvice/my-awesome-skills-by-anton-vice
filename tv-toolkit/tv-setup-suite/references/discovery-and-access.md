# Discovery, pairing and setup access

## Find and identify

The TV must be powered on and the computer on the same reachable LAN. Standby discovery varies. First inspect the current interface, routing and known neighbors:

```bash
# macOS examples:
route -n get default
ifconfig en0
arp -an
dns-sd -B _androidtvremote2._tcp local.
dns-sd -B _googlecast._tcp local.
```

Use the actual route/interface, not assumed `en0` or a fixed /24. `dns-sd` continues until stopped: bound the observation and stop it after gathering results. Resolve a discovered instance with `dns-sd -L INSTANCE SERVICE local.`. On Linux use `ip route`, `ip addr`, `ip neigh` and `avahi-browse`. If mDNS is blocked, inspect the router's device list or SSDP/UPnP descriptions for model/manufacturer. Use a bounded scan of the user's own directly connected network only if passive discovery is insufficient and within scope.

Correlate IP, manufacturer, model and mDNS/SSDP identity with the physical screen. ARP may contain stale and link-local duplicates for the same MAC; prefer the reachable LAN address and verify live device identity. Store its hardware identity privately for later rediscovery; do not paste the original TV's IP/MAC into reusable code.

Cast discovery does not establish Android: Vizio also advertises Cast and AirPlay. Confirm platform through the device Settings/model documentation and authorized service responses. Typical Android Remote v2 uses 6466/control and 6467/pairing; legacy ADB is often 5555. SSH is neither required nor usually available. Do not attempt guessed credentials, root exploits or unsupported firmware flashing to obtain setup access.

## Pair normal remote control

`scripts/remote.py` is a generic version of the original helper. Install its dependency in a dedicated Python venv using `scripts/requirements.txt`, then:

```bash
# From this skill's directory; use this session's verified IP and a private directory per TV:
.venv/bin/python scripts/remote.py --host "$TV_HOST" --state-dir private/tv-one pair
.venv/bin/python scripts/remote.py --host "$TV_HOST" --state-dir private/tv-one keyboard
```

Read the fresh on-screen code and enter it in the local terminal. The helper uses private cert/key files in a 0700 directory, 0600 files, no voice transport and no cloud account. Never commit those files, pairing codes or device dumps. Do not send a new pairing request if existing pairing still works. A code belongs to a particular live request; ask for a fresh code when retrying a failed request rather than reusing an expired one.

Use arrows/Enter, Home `h`, Back `b`, Settings `s`, volume `+/-`, mute `m` and quit `q`. It only captures input while its terminal has focus. `app youtube` targets SmartTube if installed, `app netflix` Netflix and `app movies` Lampa; adapt the helper's APPS mapping if the owner uses different clients. No auto-start/background Mac service is installed.

## Authorize temporary setup debugging

On Android/Google TV: Settings → System/About → select Android TV OS build seven times, then Developer options. Some sets need **USB debugging enabled even for legacy network ADB**. If network/wireless debugging is separately offered, follow that version's pairing process; do not assume port 5555.

For legacy network access:

```bash
adb connect "$TV_HOST:5555"
adb devices -l
```

Accept **Allow USB debugging?** on the TV for this computer. `unauthorized` is not a successful shell; wait for the physical prompt. For modern wireless debugging use the displayed pairing IP/port with `adb pair` and its separate connection port with `adb connect`. Do not disable authorization or expose ADB through the router.

Set `TV_SERIAL` to the exact authorized serial from `adb devices` and use `adb -s "$TV_SERIAL"` everywhere. Read `ro.product.manufacturer`, model, device, Android SDK, firmware/build fingerprint, `ro.product.cpu.abilist` and active user to prove the target. Save a private baseline and recovery before mutation. On macOS, a Local Network permission block may look like routing failure: verify permissions/address/subnet before repeatedly scanning or assuming a closed port.

## Handover and closure

Keep ADB available through recovery-sensitive Home/network changes and the normal reboot test. Use paired Remote v2 for daily control afterward. Turn wireless/network debugging off using the device's supported UI, revoke setup authorizations when requested, and turn USB debugging off physically. A refused port confirms no listener at that address/time; a timeout or missing mDNS record proves neither closure nor reboot. Confirm the physical settings and verify paired controls still work.
