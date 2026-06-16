# lc-guard — Deactivation

Run these commands in order.

```bash
# 1. Stop the running daemon
launchctl bootout gui/$(id -u)/com.lcguard.daemon

# 2. Unlock the plist (chflags uchg was set on install to prevent casual deletion)
chflags nouchg ~/Library/LaunchAgents/com.lcguard.daemon.plist

# 3. Remove the plist so it does not reload on reboot
rm ~/Library/LaunchAgents/com.lcguard.daemon.plist

# 4. Remove session state and config
rm -rf ~/.lc-guard/
```

After step 3, lc-guard will not start on reboot. After step 4, all session history is gone.

To verify the daemon is no longer running:
```bash
launchctl print gui/$(id -u)/com.lcguard.daemon
```
`Could not find service` means it is gone.
