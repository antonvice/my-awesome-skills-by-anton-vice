#!/usr/bin/env python3
"""Pair with and control a Google TV using its existing remote service."""

import argparse
import asyncio
import json
import os
from pathlib import Path

from androidtvremote2 import AndroidTVRemote, CannotConnect, ConnectionClosed, InvalidAuth


APPS = {"youtube": "market://launch?id=org.smarttube.stable", "netflix": "market://launch?id=com.netflix.ninja", "movies": "market://launch?id=top.rootu.lampa"}
KEYS = {
    "up": "DPAD_UP", "down": "DPAD_DOWN", "left": "DPAD_LEFT", "right": "DPAD_RIGHT",
    "ok": "DPAD_CENTER", "home": "HOME", "back": "BACK", "settings": "SETTINGS",
    "play": "MEDIA_PLAY_PAUSE", "+": "VOLUME_UP", "-": "VOLUME_DOWN", "mute": "VOLUME_MUTE",
}


async def send_key(remote, host, key):
    remote.send_key_command(key)


async def launch_app(remote, host, name):
    remote.send_launch_app_command(APPS[name])


def status(remote):
    print(json.dumps({"device": remote.device_info, "on": remote.is_on, "app": remote.current_app}, default=str), flush=True)


async def keyboard(remote, host):
    import curses

    screen = curses.initscr()
    try:
        curses.noecho()
        curses.cbreak()
        curses.set_escdelay(25)
        screen.keypad(True)
        screen.timeout(250)
        mappings = {
            curses.KEY_UP: "DPAD_UP", curses.KEY_DOWN: "DPAD_DOWN",
            curses.KEY_LEFT: "DPAD_LEFT", curses.KEY_RIGHT: "DPAD_RIGHT",
            curses.KEY_ENTER: "DPAD_CENTER", "\n": "DPAD_CENTER", "\r": "DPAD_CENTER",
            "h": "HOME", "b": "BACK", "\x1b": "BACK", "s": "SETTINGS",
            "p": "MEDIA_PLAY_PAUSE", " ": "MEDIA_PLAY_PAUSE",
            "+": "VOLUME_UP", "-": "VOLUME_DOWN", "m": "VOLUME_MUTE",
        }
        remote.keep_reconnecting()
        previous = None
        while True:
            current = (remote.is_on, remote.current_app)
            if current != previous:
                screen.erase()
                rows, width = screen.getmaxyx()
                lines = [
                    "Android TV Remote", "",
                    "Arrows: navigate   Enter: OK   h: Home   b/Esc: Back",
                    "y: YouTube   n: Netflix   l: Movies   p/Space: Play/Pause",
                    "+/-: Volume   m: Mute   s: Settings   q: Quit", "",
                    f"TV on: {remote.is_on}   App: {remote.current_app or '(not reported)'}",
                    "Controls work while this Terminal window has focus.",
                ]
                for index, line in enumerate(lines[:max(0, rows - 1)]):
                    screen.addstr(index, 0, line[:max(0, width - 1)])
                screen.refresh()
                previous = current
            try:
                key = await asyncio.to_thread(screen.get_wch)
            except curses.error:
                continue
            if key == "q":
                break
            if key in mappings:
                await send_key(remote, host, mappings[key])
            elif key in {"y", "n", "l"}:
                await launch_app(remote, host, {"y": "youtube", "n": "netflix", "l": "movies"}[key])
    finally:
        screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("command", choices=["pair", "status", "key", "app", "remote", "keyboard"])
    parser.add_argument("values", nargs="*")
    args = parser.parse_args()
    state = args.state_dir.expanduser().resolve()
    state.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(state, 0o700)
    remote = AndroidTVRemote("TV Toolkit Remote", str(state / "cert.pem"), str(state / "key.pem"), args.host, enable_voice=False)
    await remote.async_generate_cert_if_missing()
    for path in state.iterdir():
        os.chmod(path, 0o600)
    try:
        if args.command == "pair":
            await asyncio.wait_for(remote.async_start_pairing(), timeout=15)
            print("PAIRING REQUEST SENT. Read the code on the TV.", flush=True)
            while True:
                code = (await asyncio.to_thread(__import__("getpass").getpass, "TV pairing code: ")).strip()
                if not code:
                    continue
                try:
                    await remote.async_finish_pairing(code)
                    print("PAIRING COMPLETE", flush=True)
                    break
                except InvalidAuth:
                    print("Code did not match. Read the current code on the TV.", flush=True)
        await asyncio.wait_for(remote.async_connect(), timeout=15)
        status(remote)
        if args.command == "keyboard":
            await keyboard(remote, args.host)
        elif args.command == "key":
            if not args.values or any(value.lower() not in KEYS for value in args.values):
                raise ValueError("Choose keys from: " + ", ".join(KEYS))
            for value in args.values:
                await send_key(remote, args.host, KEYS[value.lower()])
                await asyncio.sleep(0.2)
        elif args.command == "app":
            if len(args.values) != 1 or args.values[0].lower() not in APPS:
                raise ValueError("Choose " + ", ".join(APPS))
            await launch_app(remote, args.host, args.values[0].lower())
            await asyncio.sleep(2)
            status(remote)
        elif args.command == "remote":
            print("Commands: up/down/left/right/ok, home/back/settings, play, +/-, mute, youtube/netflix/movies, status, text WORDS, quit", flush=True)
            remote.keep_reconnecting()
            while True:
                line = (await asyncio.to_thread(input, "TV> ")).strip()
                if line == "quit":
                    break
                if line in KEYS:
                    await send_key(remote, args.host, KEYS[line])
                elif line in APPS:
                    await launch_app(remote, args.host, line)
                elif line == "status":
                    status(remote)
                elif line.startswith("text "):
                    remote.send_text(line[5:])
                else:
                    print("Unknown command", flush=True)
        await asyncio.sleep(0.3)
    finally:
        remote.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (CannotConnect, ConnectionClosed, InvalidAuth, TimeoutError, ValueError) as error:
        raise SystemExit(f"TV connection failed: {error}") from None
    except (KeyboardInterrupt, EOFError):
        pass
