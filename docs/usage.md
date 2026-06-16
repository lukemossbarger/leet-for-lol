# lc-guard — Usage

All commands run from the project root. Prefix every command with `.venv/bin/python`.

---

## Setup (first time)

```bash
# Create venv and install dependencies
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Set your LeetCode username
.venv/bin/python lc_guard.py config username <your-lc-username>

# Install and start the daemon (do NOT use sudo — see docs/setup.md)
.venv/bin/python lc_guard.py daemon install
```

---

## Daily use

```bash
# Solve a LeetCode problem, then run this to unlock a session
.venv/bin/python lc_guard.py unlock

# Check session status at any time
.venv/bin/python lc_guard.py status
```

**Session budgets:**

| Difficulty | Games | Time   |
|------------|-------|--------|
| Easy       | 1     | 60 min |
| Medium     | 2     | 90 min |
| Hard       | 3     | 120 min |

Solving another problem while a session is active extends it — whichever budget is more generous wins.

---

## Daemon management

```bash
# Check if daemon is running
.venv/bin/python lc_guard.py daemon status

# Stop the daemon (Riot Client unblocked until restarted)
.venv/bin/python lc_guard.py daemon stop

# Start the daemon
.venv/bin/python lc_guard.py daemon start

# Restart
.venv/bin/python lc_guard.py daemon restart
```

Daemon logs: `~/.lc-guard/daemon.log`

---

## Diagnostic scripts

```bash
# Check your LeetCode submissions and see raw API data
.venv/bin/python scripts/check_submissions.py <lc-username>

# Live dashboard of monitored processes (refreshes every 2s)
.venv/bin/python scripts/watch_processes.py

# Test the process kill mechanism against real Riot/League processes
.venv/bin/python scripts/test_kill.py
```

---

## Tests

Tests were run in two ways:
- Tons of unit tests for individual functions
- Scripts to test how each part of the system (monitor, state manager, lc API, CLI) actually worked

The latter were like a psuedo e2e test for each part of the system before the entire thing could be run together.
I tried to make development of each part as orthogonal as possible.


---

## Deactivation

See `docs/deactivation.md` for the exact commands.
