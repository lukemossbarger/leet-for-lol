from .client import LeetCodeAPIError, fetch_difficulty, fetch_recent_ac
from .models import Submission, VerifyError, VerifyErrorReason


def verify(
    username: str,
    not_before: int,
    used_ids: list[str],
) -> Submission | VerifyError:

    #not_before submissions before this are rejected
    # used_ids has problem IDs already used to unlock a session today

    try:
        raw = fetch_recent_ac(username)
    except LeetCodeAPIError as e:
        return VerifyError(VerifyErrorReason.API_ERROR, str(e))
    

    if not raw:
        return VerifyError(VerifyErrorReason.NONE_FOUND, "no accepted submissions on record")

    after_cutoff = [s for s in raw if int(s["timestamp"]) > not_before]
    if not after_cutoff:
        return VerifyError(
            VerifyErrorReason.ALL_TOO_OLD,
            f"all submissions at or before cutoff {not_before}",
        )

    unused = [s for s in after_cutoff if s["id"] not in used_ids]
    if not unused:
        return VerifyError(VerifyErrorReason.ALL_USED, "all valid submissions already used today")

    best = max(unused, key=lambda s: int(s["timestamp"]))



    try:
        difficulty = fetch_difficulty(best["titleSlug"])
    except LeetCodeAPIError as e:
        return VerifyError(VerifyErrorReason.API_ERROR, str(e))
    

    return Submission(
        problem_id=best["id"],
        title=best["title"],
        title_slug=best["titleSlug"],
        difficulty=difficulty,
        submitted_at=int(best["timestamp"]),
    )
