import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from verifier.client import LeetCodeAPIError, fetch_difficulty, fetch_recent_ac


def main():
    if len(sys.argv) < 2:
        print("usage: python scripts/check_submissions.py <leetcode-username>")
        sys.exit(1)

    username = sys.argv[1]
    print(f"Fetching recent accepted submissions for: {username}\n")

    try:
        submissions = fetch_recent_ac(username)
    except LeetCodeAPIError as e:
        print(f"API error: {e}")
        sys.exit(1)

    if not submissions:
        print("No accepted submissions found.")
        sys.exit(0)

    print(f"Found {len(submissions)} submission(s):\n")
    for i, s in enumerate(submissions, 1):
        ts = int(s["timestamp"])
        from datetime import datetime, timezone
        dt = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        status = s.get("statusDisplay", "?")
        print(f"  [{i}] id={s['id']}  status={status!r}  title={s['title']!r}  slug={s['titleSlug']!r}  ts={ts} ({dt})")

    print()

    best = max(submissions, key=lambda s: int(s["timestamp"]))
    print(f"Fetching difficulty for most recent: {best['title']!r} ({best['titleSlug']})")
    try:
        difficulty = fetch_difficulty(best["titleSlug"])
        print(f"  Difficulty: {difficulty.value}")
    except LeetCodeAPIError as e:
        print(f"  Difficulty fetch failed: {e}")

    print("\nRaw JSON (first entry):")
    print(json.dumps(submissions[0], indent=2))


if __name__ == "__main__":
    main()
