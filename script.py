import argparse
import sys
import json
import os
from datetime import datetime
from lib.ctfd import CTFdScraper
from lib.justctf import JustCTFScraper
from lib.xctf import XCTFScraper
from lib.perf import PerfomanceCalculator

PLATFORMS = {"ctfd": CTFdScraper, "justctf": JustCTFScraper, "xctf": XCTFScraper}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("date")
    parser.add_argument("url")
    parser.add_argument("--platform", default="ctfd")
    parser.add_argument("--session")

    args = parser.parse_args()
    if args.platform not in PLATFORMS:
        print("Currently supported platforms are: {}".format(PLATFORMS.keys()), file=sys.stderr)
        quit(1)

    date = int(datetime.strptime(args.date, "%Y-%m-%d").timestamp())
    scraper = PLATFORMS[args.platform](args.url, session=args.session)
    teams, challenges = scraper.teams_chals()

    if os.path.exists("./ctf.json"):
        with open("./ctf.json", "r") as f:
            ctf = json.load(f)
    else:
        ctf = {"teams": {}, "events": []}

    team_standings = [t[0] for t in sorted(teams.items(), key=lambda x: len(x[1]), reverse=True)]

    perf = PerfomanceCalculator(ctf["teams"])
    team_perfs = perf.calc_performance(team_standings)
    for i in range(len(team_standings)):
        t = team_standings[i]
        p = team_perfs[i]
        rating = perf.calc_new_rating(t, p)
        if t not in ctf["teams"]:
            ctf["teams"][t] = []

        ctf["teams"][t].append({
            "event": args.name,
            "performance": p,
            "rating": rating,
            "solves": teams[t],
            "rank": i+1,
        })

    ctf["events"].append({
        "name": args.name,
        "date": date,
        "challenges": challenges,
    })
    with open("./ctf.json", "w") as f:
        json.dump(ctf, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
