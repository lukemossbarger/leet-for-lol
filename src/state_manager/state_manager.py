import dataclasses
import json
import logging
import time
from datetime import date, datetime
from pathlib import Path
from verifier.models import Submission
from .models import BUDGETS, SessionState
logger = logging.getLogger(__name__)
DEFAULT_STATE_PATH = Path.home() / ".lc-guard" / "state.json"


def _empty(today: str) -> SessionState:
    return SessionState(
        active=False,
        date=today,
        expiry=0,
        games_remaining=0,
        difficulty="",
        used_problem_ids=[],
    )




class StateManager:
    def __init__(self, state_path: Path = DEFAULT_STATE_PATH):
        self._path = state_path
        self._path.parent.mkdir(parents=True, exist_ok=True)


    def get(self) -> SessionState:
        state = self._read()
        today = date.today().isoformat()


        if state.date != today:
            midnight = int(datetime.combine(date.today(), datetime.min.time()).timestamp())
            state = dataclasses.replace(_empty(today), last_grant_time=midnight)
            self._write(state)
            logger.info("midnight reset — session cleared")
            return state

        if state.active:
            now = int(time.time())
            if now >= state.expiry or state.games_remaining <= 0:
                state = dataclasses.replace(state, active=False)
                self._write(state)
                logger.info("session expired")

        return state



    def grant(self, submission: Submission) -> SessionState:
        current = self.get()
        budget = BUDGETS[submission.difficulty]
        now = int(time.time())
        new_expiry = now + budget.minutes * 60


        if current.active:
            games = max(current.games_remaining, budget.games)
            expiry = max(current.expiry, new_expiry)
            logger.info("session extended — games=%d expiry=%d", games, expiry)
        else:
            games = budget.games
            expiry = new_expiry
            logger.info("session granted — %s games=%d", submission.difficulty.value, games)


        state = SessionState(
            active=True,
            date=current.date,
            expiry=expiry,
            games_remaining=games,
            difficulty=submission.difficulty.value,
            used_problem_ids=current.used_problem_ids + [submission.problem_id],
            last_grant_time=now,
        )

        self._write(state)
        return state

    def decrement_game(self) -> SessionState:
        state = self.get()
        if not state.active:
            return state
        new_games = max(0, state.games_remaining - 1)
        state = dataclasses.replace(state, games_remaining=new_games)
        self._write(state)
        logger.info("game decremented — games_remaining=%d", new_games)
        return state

    def _read(self) -> SessionState:
        try:
            data = json.loads(self._path.read_text())
            return SessionState(**data)
        except Exception:
            logger.warning("state file unreadable — failing open")
            return _empty(date.today().isoformat())


    def _write(self, state: SessionState) -> None:
        with open(self._path, 'w') as f:
            json.dump(dataclasses.asdict(state), f, indent=2)
