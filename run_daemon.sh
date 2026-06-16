#!/bin/bash
export VIRTUAL_ENV="/Users/lukemossbarger/lc-guard/.venv"
export PATH="$VIRTUAL_ENV/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin"
export HOME="/Users/lukemossbarger"
exec "$VIRTUAL_ENV/bin/python" "/Users/lukemossbarger/lc-guard/daemon_runner.py"
