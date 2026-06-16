import os
import pwd
import subprocess
import sys
from pathlib import Path

PLIST_LABEL = "com.lcguard.daemon"
_DAEMON_SCRIPT = (Path(__file__).parent.parent.parent / "daemon_runner.py").resolve()


def _actual_user() -> str:
    return os.environ.get("SUDO_USER") or os.environ.get("USER") or pwd.getpwuid(os.getuid()).pw_name


def _actual_uid() -> int:
    return pwd.getpwnam(_actual_user()).pw_uid



def _actual_home() -> Path:
    return Path(pwd.getpwnam(_actual_user()).pw_dir)


def _log_dir() -> Path:
    return _actual_home() / ".lc-guard"


def _plist_dest() -> Path:
    return _actual_home() / "Library" / "LaunchAgents" / "com.lcguard.daemon.plist"



def generate_plist() -> str:
    log = _log_dir()
    wrapper = (Path(__file__).parent.parent.parent / "run_daemon.sh").resolve()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{PLIST_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>{wrapper}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{log}/daemon.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>{log}/daemon.stderr.log</string>
</dict>
</plist>
"""


def _launchctl(*args: str) -> tuple[int, str]:
    result = subprocess.run(["launchctl", *args], capture_output=True, text=True)
    return result.returncode, (result.stdout + result.stderr).strip()


def install() -> tuple[bool, str]:
    log = _log_dir()
    log.mkdir(parents=True, exist_ok=True)



    actual_uid = _actual_uid()
    for fname in ("daemon.stdout.log", "daemon.stderr.log"):
        p = log / fname
        if not p.exists():
            p.touch(mode=0o644)
        os.chown(p, actual_uid, -1)

    dest = _plist_dest()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(generate_plist())
    dest.chmod(0o644)
    subprocess.run(["chflags", "uchg", str(dest)], check=False)

    uid = actual_uid
    code, out = _launchctl("bootstrap", f"gui/{uid}", str(dest))
    if code != 0:
        return False, f"launchctl bootstrap failed: {out}"
    return True, "Daemon installed and started."


def start() -> tuple[bool, str]:
    uid = _actual_uid()
    code, out = _launchctl("kickstart", f"gui/{uid}/{PLIST_LABEL}")
    return code == 0, out or "Daemon started."


def stop() -> tuple[bool, str]:
    uid = _actual_uid()
    code, out = _launchctl("kill", "TERM", f"gui/{uid}/{PLIST_LABEL}")
    return code == 0, out or "Daemon stopped."


def restart() -> tuple[bool, str]:
    stop()
    return start()


def status() -> tuple[bool, str]:
    uid = _actual_uid()
    code, out = _launchctl("print", f"gui/{uid}/{PLIST_LABEL}")
    if code != 0:
        return False, "Daemon not running."
    for line in out.splitlines():
        if "state" in line.lower():
            return True, line.strip()
    return True, "Running."
