import time
import psutil

LAUNCHER_PROCESS_NAMES = {"RiotClientServices", "LeagueClient"}
GAME_PROCESS_NAME = "LeagueofLegends"


def is_game_running() -> bool:
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.name() == GAME_PROCESS_NAME:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False



def get_launcher_pids() -> list[int]:
    pids = []
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.name() in LAUNCHER_PROCESS_NAMES:
                pids.append(proc.pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return pids


def get_launcher_details() -> list[dict]:
    details = []
    for proc in psutil.process_iter(["name", "pid", "status", "create_time"]):
        try:
            if proc.name() in LAUNCHER_PROCESS_NAMES:
                details.append({
                    "name": proc.name(),
                    "pid": proc.pid,
                    "status": proc.status(),
                    "uptime": int(time.time() - proc.create_time()),
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return details



def get_game_details() -> dict | None:
    for proc in psutil.process_iter(["name", "pid", "status", "create_time"]):
        try:
            if proc.name() == GAME_PROCESS_NAME:
                return {
                    "name": proc.name(),
                    "pid": proc.pid,
                    "status": proc.status(),
                    "uptime": int(time.time() - proc.create_time()),
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None


def kill_process(pid: int) -> None:
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
    except psutil.TimeoutExpired:
        try:
            proc.kill()
        except psutil.NoSuchProcess:
            pass
    except psutil.NoSuchProcess:
        pass
