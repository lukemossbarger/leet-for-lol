from dataclasses import dataclass, field

from verifier.models import Difficulty


@dataclass
class Budget:
    games: int
    minutes: int


BUDGETS: dict[Difficulty, Budget] = {
    Difficulty.EASY:   Budget(games=1, minutes=60),
    Difficulty.MEDIUM: Budget(games=2, minutes=90),
    Difficulty.HARD:   Budget(games=3, minutes=120),
}



@dataclass
class SessionState:
    active: bool
    date: str
    expiry: int
    games_remaining: int
    difficulty: str
    used_problem_ids: list[str] = field(default_factory=list)
    last_grant_time: int = 0
