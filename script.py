import argparse
import sys
import json
import os
from typing import List
from datetime import datetime
from lib.ctfd import CTFdScraper
from lib.ctfd_legacy import CTFdLegacyScraper
from lib.justctf import JustCTFScraper
from lib.xctf import XCTFScraper
from lib.rctf import RCTFScraper
from lib.perf import PerfomanceCalculator
from lib.difficulty import calc_difficulty

PLATFORMS = {"ctfd": CTFdScraper, "ctfd-legacy": CTFdLegacyScraper, "justctf": JustCTFScraper, "xctf": XCTFScraper, "rctf": RCTFScraper}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("date")
    parser.add_argument("url")
    parser.add_argument("--platform", default="ctfd")
    parser.add_argument("--session")
    parser.add_argument("--mode", default="teams")

    args = parser.parse_args()
    if args.platform not in PLATFORMS:
        print("Currently supported platforms are: {}".format(PLATFORMS.keys()), file=sys.stderr)
        quit(1)

    date = int(datetime.strptime(args.date, "%Y-%m-%d").timestamp())
    scraper = PLATFORMS[args.platform](args.url, session=args.session, mode=args.mode)
    team_standings, teams, challenges = scraper.teams_chals()

    if os.path.exists("./ctf.json"):
        with open("./ctf.json", "r") as f:
            ctf = json.load(f)
    else:
        ctf = {"teams": {}, "events": {}}

    perf = PerfomanceCalculator(ctf["teams"], ctf["events"])
    team_perfs = perf.calc_performance(team_standings,)

    team_updates = {}
    for i in range(len(team_standings)):
        t = team_standings[i]
        p = team_perfs[i]
        rating = perf.calc_new_rating(t, p)
        team_updates[t] = {
            "event": args.name,
            "performance": p,
            "rating": rating,
            "solves": teams[t],
            "rank": i+1,
        }

    for t, update in team_updates.items():
        if t not in ctf["teams"]:
            ctf["teams"][t] = {"name": t, "events": {}, "rating": 0}
        ctf["teams"][t]["events"][args.name] = update
        ctf["teams"][t]["rating"] = update["rating"]

    for c_id in challenges.keys():
        diff = calc_difficulty(c_id, [t for t in team_updates.values()])
        challenges[c_id]["difficulty"] = diff

    ctf["events"][args.name] = {
        "name": args.name,
        "date": date,
        "challenges": challenges,
    }
    with open("./ctf.json", "w") as f:
        json.dump(ctf, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
