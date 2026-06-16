# lc-guard — Setup Guide

## What it does

lc-guard blocks the Riot Client (League of Legends launcher) until you solve a LeetCode problem. Solve one, run `lc-guard unlock`, play your games. When the session expires, it kills the client until you solve another.

---

## Prerequisites

- **macOS**
- **Python**
- **LoL / Riot Client**
- **LeetCode** username

---

## 1. Get Code

```bash
git clone https://github.com/your-username/lc-guard.git
cd lc-guard
```

---

## 2. Setup venv / dependencies

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

---

## 3. Configure lc-guard with LeetCode username

```bash
.venv/bin/python lc_guard.py config username <your_leetcode_username>
```

---

## 4. Install the daemon

The daemon is a background process that watches for the Riot Client and kills it if you don't haven't unlocked a session.

```bash
.venv/bin/python lc_guard.py daemon install
```

**Do not run this with `sudo`.** It installs a user-level background service that runs as you. Using `sudo` creates log files owned by root that launchd (which runs as your user) cannot write to, causing the daemon to fail.

What this does:
- Writes config file to `~/Library/LaunchAgents/com.lcguard.daemon.plist`
- Registers and starts daemon with macOS's launchd system
- The daemon starts automatically on every login

**When you get a notification for a new program to run in the background, super important you click yes.**
**If you press no or let it expire, go to System Settings->General->Login Items and flick the switch for `bash` on.**

---

## 5. Verify it's running

```bash
.venv/bin/python lc_guard.py daemon status
```

You should see something like `state = running`. If it says `not running`, check `~/.lc-guard/daemon.log` for errors.

```bash
.venv/bin/python lc_guard.py status
```

Should print `Session: LOCKED`, meaning the daemon is active and blocking the Riot Client / LoL.

---

## 6. Test the block

Try starting League of Legends. The Riot Client should launch briefly and then be killed. You'll need to run `lc-guard unlock` to play now.

---

## Daily use

1. Solve a LeetCode problem and submit it (must be **Accepted**)
2. Wait a few seconds for LeetCode to record the submission
3. Run:

```bash
.venv/bin/python lc_guard.py unlock
```

If a valid submission is found, you'll see the problem name, difficulty, and session details:

```
Unlocked: Two Sum (Easy)
  Games: 1  |  Expires: 09:45 PM
```

4. Open the Riot Client and play. The daemon tracks your games and closes the session when time or game count runs out. If you are actively in a match when the time runs out, there is a grace period that stops the daemon from killing your process. No LP loss for a match that goes on too long.

**Session budgets:**

| Difficulty | Games allowed | Time window |
|------------|---------------|-------------|
| Easy       | 1             | 60 min      |
| Medium     | 2             | 90 min      |
| Hard       | 3             | 120 min     |

Solving another problem while a session is active extends it — whichever of the current and new budgets is more generous applies.

---

## Troubleshooting

**`Unlock failed: No accepted submissions found`**
Your LeetCode account has no accepted submissions, or none submitted after your last session. Solve a problem and submit it.

**`Unlock failed: All submissions predate your last session grant`**
You solved the problem before your last unlock. Solve a new one.

**`Unlock failed: All valid submissions already used today`**
You've already used every valid submission today. Solve another problem.

**Riot Client opens but isn't killed**
The daemon may not be running. Check:
```bash
.venv/bin/python lc_guard.py daemon status
cat ~/.lc-guard/daemon.log
```

**Daemon won't start / keeps crashing**
Check the log:
```bash
cat ~/.lc-guard/daemon.log
cat ~/.lc-guard/daemon.stderr.log
```

If `daemon.stdout.log` or `daemon.stderr.log` are owned by root (you'll see `root` in `ls -la ~/.lc-guard/`), delete them and reinstall:
```bash
rm ~/.lc-guard/daemon.stdout.log ~/.lc-guard/daemon.stderr.log
.venv/bin/python lc_guard.py daemon install
```

---

## Deactivation

To remove lc-guard completely, see `docs/deactivation.md`.
