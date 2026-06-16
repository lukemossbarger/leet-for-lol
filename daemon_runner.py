import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from monitor import Monitor
from state_manager import StateManager

_LOG_DIR = Path.home() / ".lc-guard"
_LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.FileHandler(_LOG_DIR / "daemon.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def main():
    sm = StateManager()
    monitor = Monitor(sm)
    monitor.run()


if __name__ == "__main__":
    main()
