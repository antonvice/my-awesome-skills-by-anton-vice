---
name: tv-cleanyourtv-launcher
description: Install CleanYourTV as Android TV or Google TV Home, apply a lightweight cyberpunk glass-dock theme and repair physical remote shortcuts with a reversible, verified launcher handover.
---

# CleanYourTV cyberpunk Home

Install the final launcher used in the reference setup: [CleanYourTV](https://github.com/Gathin23/cleanyourtv), package `com.gathin.tvhome`. This changes the Home app, not the factory OS. Do not substitute Couchy or keep a stock-Home redirect that visibly flashes unless the user knowingly prefers that compromise.

## Prepare

Discover the current TV address via mDNS/ARP, confirm Android/Google TV and supported SDK/ABI, and obtain on-TV ADB authorization. Select the serial explicitly. Save the current Home component, enabled/default states of stock launchers and setup packages, accessibility-service list and state, relevant permissions/app-ops and private Wi-Fi ownership evidence before running an installer. Its own package-list snapshot is not a substitute for this pre-install record.

Read [handover and remote procedure](references/handover-and-remote.md) before changing Home. The original reviewed revision was `6ffa7fa5df7c38714cd89fd77fe636c53e759083` (Android 8+ at that revision); check API/build requirements for another revision. Fetch source, review the installer/permissions, and build with JDK 17 and the required Android SDK. Follow upstream build, test and lint commands. Do not weaken platform permissions or skip build failures to reach installation.

## Install and hand over Home

Use the supported build/install tools. First install and launch the new activity successfully while stock Home is still available. Handle setupwraith ownership/interception using the reference procedure **before** permitting an installer to disable the stock launcher. Require both foreground activity evidence and physical Home testing. An Android Home role assignment alone failed on the original firmware.

For special buttons, preserve OEM key services first. Enable only the needed key-only accessibility helper within the user's authorized scope, explaining persistence and the optional secure-settings recovery grant. Keep unrelated accessibility services intact. Verify the installed helper's metadata denies window-content retrieval. Adding a helper is not permission to enable voice, capture audio or read app contents.

Apply the theme with upstream `tools/theme.sh`, not direct writes into another app's private storage. Read [theme notes](references/theme.md). Start from [assets/cyberpunk/config.json](assets/cyberpunk/config.json) and its wallpaper; adapt dock apps, hidden apps and key mappings to this owner's installed apps and preference. The historical Netflix/SmartTube/Lampa/AirPlay dock is an example, not a keep-only list. Keep the app library and native Settings reachable.

Remove any installer-granted fine-location access if the network-name pill is not wanted, as in the source setup. Verify the actual installed launcher has no INTERNET, microphone or camera permission; do not infer this from its name. Theme-helper recovery may need a scoped WRITE_SECURE_SETTINGS grant, which must be recorded for rollback.

## Verify and recover

- From several apps and HDMI, press physical Home repeatedly: CleanYourTV must appear directly, without Google Home flicker or a setup recovery loop.
- Test physical Back, Settings, Input, Netflix/desired app shortcuts, YouTube/SmartTube, volume tap and hold. Capture actual scan codes where needed; never assume the example remote's codes are universal.
- Reboot and prove it with uptime. Recheck Wi-Fi, Home owner/foreground, helper binding, key behavior and the selected theme. A successful `am start` is not user confirmation of the remote or picture.
- Preserve each existing app's data and functions. If Home/keys/Wi-Fi fail, restore recorded package/Home/helper state before continuing. Don't permanently delete the old system launcher or setup wizard.
- Keep the pre-handover record, exact upstream revision, theme and recovery commands private; close temporary debugging after any remaining setup. Report any test awaiting the owner.

The default theme intentionally uses static artwork and low effects for weak hardware. If the user asks for animation, add one effect at a time, measure navigation/PSS and keep the faster style if effects regress it.
