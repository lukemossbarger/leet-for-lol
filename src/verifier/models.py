from dataclasses import dataclass
from enum import Enum


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class VerifyErrorReason(Enum):
    NONE_FOUND = "no accepted submissions found"
    ALL_TOO_OLD = "all submissions predate the last session"
    ALL_USED = "all valid submissions already used today"
    API_ERROR = "could not reach LeetCode API"



@dataclass(frozen=True)
class Submission:
    problem_id: str
    title: str
    title_slug: str
    difficulty: Difficulty
    submitted_at: int



@dataclass(frozen=True)
class VerifyError:
    reason: VerifyErrorReason
    detail: str
