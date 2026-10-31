"""Fetch the contribution calendar of a GitHub user into data/contributions.json."""
import json
import os
import urllib.request

USER = os.environ.get("GH_USER", "gabsh")
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""
LEVELS = {"NONE": 0, "FIRST_QUARTER": 1, "SECOND_QUARTER": 2, "THIRD_QUARTER": 3, "FOURTH_QUARTER": 4}

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
    headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json", "User-Agent": "profile-art"},
)
with urllib.request.urlopen(req) as r:
    payload = json.load(r)
if "errors" in payload:
    raise SystemExit(payload["errors"])

cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
out = {
    "user": USER,
    "total": cal["totalContributions"],
    "weeks": [
        [{"date": d["date"], "count": d["contributionCount"], "level": LEVELS[d["contributionLevel"]]}
         for d in w["contributionDays"]]
        for w in cal["weeks"]
    ],
}
os.makedirs("data", exist_ok=True)
with open("data/contributions.json", "w") as f:
    json.dump(out, f)
print(f"{USER}: {out['total']} contributions")
