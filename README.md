# My Awesome Skills by Anton Weiss

My collection of practical skills for AI coding agents. Each skill packages a workflow that I have used, the details that made it work, and the checks needed to tell whether it actually worked.

## TV Toolkit

The first skill set turns a compatible Android TV or Google TV into a cleaner, faster, personalized media setup. It comes from a real TCL setup: discovery on Wi-Fi, authorized debugging, reversible cleanup, a cyberpunk CleanYourTV Home screen, working remote buttons, and movies through an on-demand server running on the TV itself.

| Skill | What it does |
| --- | --- |
| [tv-lampa-torrserve](tv-toolkit/tv-lampa-torrserve/SKILL.md) | Install Lampa + TorrServe/TorrServer + Just Player, with Russian UI, local control and on-demand playback. No laptop server needed. |
| [tv-privacy-optimize](tv-toolkit/tv-privacy-optimize/SKILL.md) | Audit privacy and performance, turn off optional reporting, and disable unwanted apps reversibly while preserving the owner's apps and TV functions. |
| [tv-cleanyourtv-launcher](tv-toolkit/tv-cleanyourtv-launcher/SKILL.md) | Install CleanYourTV, apply the included cyberpunk wallpaper/theme, and repair physical remote shortcuts. |
| [tv-setup-suite](tv-toolkit/tv-setup-suite/SKILL.md) | Coordinate all three from network discovery through playback, remote testing, recovery and debugging closure. |

TorrServe is the Android client; TorrServer is its streaming engine. This is **not a Tor anonymity server**. Customizing Home does **not** replace the factory Android firmware. Non-Android Vizio, Roku and similar systems cannot use these APK workflows directly.

## Use with an agent

Clone this repository, then ask an agent to read the relevant `SKILL.md`:

> Use `tv-toolkit/tv-setup-suite/SKILL.md` to discover my TV and set up this toolkit. Keep my existing apps unless I ask to remove them.

Individual skills also work independently. For Codex, install the four skill directories under your skills directory (usually `~/.codex/skills`). From the repository root:

```bash
python3 - <<'PY'
import os, shutil
from pathlib import Path
target = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills'
sources = sorted(Path('tv-toolkit').glob('*/SKILL.md'))
conflicts = [target / source.parent.name for source in sources if (target / source.parent.name).exists()]
if conflicts:
    raise SystemExit('Existing skills need review before replacement: ' + ', '.join(map(str, conflicts)))
target.mkdir(parents=True, exist_ok=True)
for source in sources:
    shutil.copytree(source.parent, target / source.parent.name)
print('Installed', len(sources), 'skills to', target)
PY
```

Invoke `$tv-setup-suite`, `$tv-lampa-torrserve`, `$tv-privacy-optimize`, or `$tv-cleanyourtv-launcher` in a host that supports that syntax. Other agents can read these Markdown instructions directly; OpenAI UI metadata is optional.

## What is included

- The final working Lampa configuration, exact historical installer hashes and source links.
- The lightweight cyberpunk theme and wallpaper used in the original setup.
- Read-only TV inventory and a generic paired Android TV remote helper.
- Dry-run-first TorrServer configuration and Lampa backup-file generation helpers.
- Recovery instructions and the failures that matter: Wi-Fi ownership, Home flicker, broken special buttons, storage permission and background startup.

App choices, language, voice controls and appearance remain configurable. The original owner's four dock apps and 38 disabled packages are historical examples, not a universal allowlist or removal target. No APKs, device credentials, network identifiers, personal screenshots, or raw device audits are distributed.

## Validation and limits

The original TCL setup had user-confirmed picture/sound, SmartTube playback, Apple mirroring, Home and special buttons, and TV-local on-demand movie playback. Final physical USB-debugging closure was still pending in that session. These skills preserve that distinction rather than treating an unavailable port as proof of a secure shutdown.

The new helpers are tested locally with fixtures and a fake local server. They have not been re-run against a live TV as part of publishing this repository. Privacy checks verify specific settings and observed activity; they do not prove that closed firmware never sends data. Torrent traffic and third-party search services are not anonymous. Use media you are authorized to access.

Run local helper tests with `python3 -m unittest discover -s tests -v`. See [TV Toolkit](tv-toolkit/README.md) for workflow and sources.

## License

Original instructions, helper code and included generated artwork are provided under [MIT](LICENSE). Linked upstream software retains its own licenses; see [THIRD_PARTY.md](THIRD_PARTY.md).
