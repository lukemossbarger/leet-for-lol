import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from monitor import (
    GAME_PROCESS_NAME,
    LAUNCHER_PROCESS_NAMES,
    get_game_details,
    get_launcher_details,
)

POLL_INTERVAL = 2


def fmt_uptime(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    return f"{seconds // 3600}h {(seconds % 3600) // 60}m"


def render(tick: int) -> None:
    launchers = get_launcher_details()
    game = get_game_details()

    lines = []
    lines.append("=" * 52)
    lines.append(f"  lc-guard process monitor  (tick {tick}, every {POLL_INTERVAL}s)")
    lines.append("=" * 52)

    lines.append("\nLAUNCHERS  (kill targets when no session)")
    lines.append("-" * 52)
    if launchers:
        for p in launchers:
            lines.append(f"  {'RUNNING':>8}  {p['name']:<22}  pid={p['pid']}  up={fmt_uptime(p['uptime'])}")
    else:
        for name in sorted(LAUNCHER_PROCESS_NAMES):
            lines.append(f"  {'not found':>8}  {name}")

    lines.append("\nGAME  (grace-period target + decrement trigger)")
    lines.append("-" * 52)
    if game:
        lines.append(f"  {'IN GAME':>8}  {game['name']:<22}  pid={game['pid']}  up={fmt_uptime(game['uptime'])}")
    else:
        lines.append(f"  {'not found':>8}  {GAME_PROCESS_NAME}")

    lines.append("\n" + "=" * 52)
    status_parts = []
    if launchers:
        status_parts.append(f"{len(launchers)} launcher(s) up")
    if game:
        status_parts.append("game in progress")
    if not launchers and not game:
        status_parts.append("all quiet")
    lines.append("  " + " | ".join(status_parts))
    lines.append("=" * 52)
    lines.append("  Ctrl+C to exit")

    sys.stdout.write("\033[2J\033[H" + "\n".join(lines) + "\n")
    sys.stdout.flush()


def main():
    tick = 0
    print("Starting watch... (first refresh in 0s)")
    while True:
        render(tick)
        tick += 1
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nStopped.")
