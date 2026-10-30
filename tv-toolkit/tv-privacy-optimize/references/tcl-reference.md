# Historical TCL candidates and dependencies

This is evidence from one BeyondTV4 / Android 11 setup. It is **not an executable debloat list**, and the source TV's 38-package count is not a goal.

| Category | Historical examples | Decide on the current TV |
| --- | --- | --- |
| Analytics/reporting | `com.tcl.bi`, `com.google.android.feedback` | Inspect service/manifest evidence and opt-ins; retain dependencies if any. |
| Voice, only with voice-off intent | `com.google.android.katniss`, `com.tcl.smartalexa`, `com.tcl.assistant` | Disabling removes voice search/assistant functionality. |
| Content/promotion portals | `com.tcl.tv.tclchannel`, `com.tcl.tv.plus`, `com.tcl.channelplus`, `com.tcl.waterfall.overseas`, `com.tcl.messagebox`, `com.tcl.esticker`, `com.tcl.usercenter` | Owner may actually use their channels, account or notices. |
| Partner setup | `com.tcl.partnercustomizer` | Inspect boot/network dependencies before considering it optional. |
| Dashboard | `com.tcl.dashboard` | The TCL HOME branded key needs a working replacement mapping if its target is removed. |
| Ambient/gallery/manual | `com.google.android.apps.tv.dreamx`, `com.tcl.gallery`, `com.tcl.ocean.instructions` | The owner may want their screensaver/photos/manual. |
| Sample browser | `org.chromium.webview_shell` | Distinguish the demo app from the **actual WebView provider**; keep the provider. |
| Entertainment apps | Previously selected streaming/music apps | Keep by default. Ask only if removal preference is unresolved. |

Do not blindly disable `com.tcl.keyhelp`, vendor key/input handlers, Settings, TV input, Bluetooth, Cast/paired remote services, DRM/media codecs, permission/package installers, update services or core content providers. `com.tcl.browser` was restored because the owner wanted BrowseHere; earlier cleanup reports listing it as removed were superseded.

The final launcher skill owns `com.google.android.apps.tv.launcherx` and `com.google.android.tungsten.setupwraith` handover. Neither belongs in a generic privacy batch. setupwraith can own saved Wi-Fi and intercept Home. `android.autoinstalls.config.google.gtvpai` remained enabled because input-driver permissions could not be verified. Retain uncertain dependencies until evidence resolves them.

When a remote regression occurs, first restore the most recent batch or original button handler and retest physical keys. Do not conclude that arrow navigation means every key works. The successful source-TV test covered Home, Netflix, YouTube/SmartTube, Settings, Input, and held Volume Down; the branded TCL HOME → Lampa mapping was confirmed separately.
