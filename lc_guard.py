#Usage: .venv/bin/python lc_guard.py <command>

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from cli.cli import main

if __name__ == "__main__":
    main()
