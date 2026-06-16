import time
from datetime import datetime
import click
from state_manager import StateManager
from verifier import Submission, VerifyError, VerifyErrorReason, verify
from . import daemon as daemon_mod
from .config import get_username, set_username


@click.group()
def cli():
    pass


@cli.command()
def unlock():
    username = get_username()
    if not username:
        click.echo("No username set. Need to use \"lc-guard config username <your-lc-username>\"")
        return

    sm = StateManager()
    state = sm.get()

    click.echo(f"Checking submissions:")
    result = verify(username, state.last_grant_time, state.used_problem_ids)

    if isinstance(result, VerifyError):
        reasons = {
            VerifyErrorReason.NONE_FOUND:  "No accepted submissions found.",
            VerifyErrorReason.ALL_TOO_OLD: "All submissions predate your last session grant.",
            VerifyErrorReason.ALL_USED:    "All valid submissions already used today.",
            VerifyErrorReason.API_ERROR:   f"LeetCode API error: {result.detail}",
        }
        click.echo(f"Unlock failed: {reasons[result.reason]}")
        return

    new_state = sm.grant(result)
    expiry_str = datetime.fromtimestamp(new_state.expiry).strftime("%I:%M %p")
    click.echo(f"Unlocked: {result.title} ({result.difficulty.value})")
    click.echo(f"  Games remaining: {new_state.games_remaining}  |  Expiry: {expiry_str}")


@cli.command()
def status():
    sm = StateManager()
    state = sm.get()

    if state.active:
        remaining = max(0, state.expiry - int(time.time()))
        mins, secs = divmod(remaining, 60)
        expiry_str = datetime.fromtimestamp(state.expiry).strftime("%I:%M %p")
        click.echo("Session: ACTIVE")
        click.echo(f"  Difficulty:      {state.difficulty}")
        click.echo(f"  Games remaining: {state.games_remaining}")
        click.echo(f"  Time remaining:  {mins}m {secs}s")
        click.echo(f"  Expires:         {expiry_str}")
    else:
        click.echo("Session: LOCKED")
        click.echo("  Run 'lc-guard unlock' to verify a LeetCode submission.")


@cli.group("config")
def config_group():
    pass


@config_group.command("username")
@click.argument("username")
def config_username(username):
    set_username(username)
    click.echo(f"Username set: {username}")


@cli.group()
def daemon():
    pass


@daemon.command("install")
def daemon_install():
    ok, msg = daemon_mod.install()
    click.echo(msg)


@daemon.command("start")
def daemon_start():
    """Start the daemon."""
    ok, msg = daemon_mod.start()
    click.echo(msg)


@daemon.command("stop")
def daemon_stop():
    ok, msg = daemon_mod.stop()
    click.echo(msg)


@daemon.command("restart")
def daemon_restart():
    ok, msg = daemon_mod.restart()
    click.echo(msg)


@daemon.command("status")
def daemon_status():
    ok, msg = daemon_mod.status()
    click.echo(msg)


def main():
    cli()
