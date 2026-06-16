import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import psutil
from monitor.processes import (
    GAME_PROCESS_NAME,
    get_game_details,
    get_launcher_pids,
    is_game_running,
    kill_process,
)


def confirm(prompt: str) -> bool:
    try:
        input(prompt)
        return True
    except KeyboardInterrupt:
        print("\nAborted.")
        return False


def kill_and_report(pids: list[int], label: str) -> bool:
    print(f"\nKilling {label}:")
    for pid in pids:
        print(f"  killing pid={pid}...", end=" ", flush=True)
        kill_process(pid)
        alive = psutil.pid_exists(pid)
        print("ALIVE (kill failed)" if alive else "DEAD")
    return True


def main():
    launcher_pids = get_launcher_pids()
    game = get_game_details()

    if not launcher_pids and not game:
        print("Nothing found. Open Riot Client first.")
        sys.exit(1)


    if launcher_pids:
        print("Found launcher processes:")
        for pid in launcher_pids:
            try:
                name = psutil.Process(pid).name()
                print(f"  {name}  pid={pid}")
            except psutil.NoSuchProcess:
                print(f"  ???  pid={pid}")
    else:
        print("No launcher processes found.")


    if game:
        print(f"\nGame in progress:")
        print(f"  {game['name']}  pid={game['pid']}  up={game['uptime']}s")
    else:
        print("\nNo game in progress.")

 
    kill_launchers = False
    if launcher_pids:
        print()
        if confirm(f"Kill {len(launcher_pids)} launcher(s)? Press Enter to confirm, Ctrl+C to skip... "):
            kill_launchers = True
            kill_and_report(launcher_pids, "launchers")


    kill_game = False
    if game:
        print()
        if confirm(f"Kill game process (pid={game['pid']})? Press Enter to confirm, Ctrl+C to skip... "):
            kill_game = True
            kill_and_report([game["pid"]], "game")

    time.sleep(0.5)
    print("\n--- Results ---")

    if kill_launchers:
        remaining = get_launcher_pids()
        if not remaining:
            print("Launchers: PASS — all gone")
        else:
            print(f"Launchers: FAIL — {len(remaining)} still running: {remaining}")

    if kill_game:
        still_running = is_game_running()
        print(f"Game:      {'FAIL — still running' if still_running else 'PASS — gone'}")


if __name__ == "__main__":
    main()
