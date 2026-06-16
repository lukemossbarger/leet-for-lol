import httpx

from .models import Difficulty

GRAPHQL_URL = "https://leetcode.com/graphql"

_RECENT_AC_QUERY = """
query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    id
    title
    titleSlug
    timestamp
    statusDisplay
  }
}
"""

_DIFFICULTY_QUERY = """
query questionDifficulty($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    difficulty
  }
}
"""

_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "lc-guard/1.0",
    "Referer": "https://leetcode.com",
}


class LeetCodeAPIError(Exception):
    pass


def fetch_recent_ac(username: str, limit: int = 20) -> list[dict]:
    payload = {
        "query": _RECENT_AC_QUERY,
        "variables": {"username": username, "limit": limit},
    }
    try:
        resp = httpx.post(GRAPHQL_URL, json=payload, headers=_HEADERS, timeout=10.0)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        raise LeetCodeAPIError(f"HTTP error: {e}") from e

    body = resp.json()
    if "errors" in body:
        raise LeetCodeAPIError(f"GraphQL errors: {body['errors']}")

    submissions = body.get("data", {}).get("recentAcSubmissionList")
    if submissions is None:
        raise LeetCodeAPIError(f"unexpected response shape: {body}")

    return submissions


def fetch_difficulty(title_slug: str) -> Difficulty:
    payload = {
        "query": _DIFFICULTY_QUERY,
        "variables": {"titleSlug": title_slug},
    }
    try:
        resp = httpx.post(GRAPHQL_URL, json=payload, headers=_HEADERS, timeout=10.0)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        raise LeetCodeAPIError(f"HTTP error: {e}") from e

    body = resp.json()
    if "errors" in body:
        raise LeetCodeAPIError(f"GraphQL errors: {body['errors']}")

    difficulty_str = (body.get("data") or {}).get("question", {}).get("difficulty")
    if not difficulty_str:
        raise LeetCodeAPIError(f"difficulty not found for slug: {title_slug!r}")

    try:
        return Difficulty(difficulty_str)
    except ValueError:
        raise LeetCodeAPIError(f"unknown difficulty value: {difficulty_str!r}")
