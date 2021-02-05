import argparse
import sys
import json
import os
from lib.ctfd import CTFdScraper
from lib.perf import PerfomanceCalculator

PLATFORMS = {"ctfd": CTFdScraper}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("url")
    parser.add_argument("--platform", default="ctfd")

    args = parser.parse_args()
    if args.platform not in PLATFORMS:
        print("Currently supported platforms are: {}".format(PLATFORMS.keys()), file=sys.stderr)
        quit(1)

    scraper = PLATFORMS[args.platform](args.url)
    teams, challenges = scraper.teams_chals()

    if os.path.exists("./ctf.json"):
        with open("./ctf.json", "r") as f:
            ctf = json.load(f)
    else:
        ctf = {"teams": {}, "challenges": []}

    team_standings = [t[0] for t in sorted(teams.items(), key=lambda x: len(x[1]), reverse=True)]

    perf = PerfomanceCalculator(ctf["teams"])
    team_perfs = perf.calc_performance(team_standings)
    for i in range(len(team_standings)):
        t = team_standings[i]
        p = team_perfs[i]
        rating = perf.calc_new_rating(t, p)
        if t not in ctf["teams"]:
            ctf["teams"][t] = {
                "events": [],
                "performances": [],
                "ratings": [],
                "solves": [],
                "standings": [],
            }
        ctf["teams"][t]["events"].append(args.name)
        ctf["teams"][t]["performances"].append(p)
        ctf["teams"][t]["ratings"].append(rating)
        ctf["teams"][t]["solves"].append(teams[t])
        ctf["teams"][t]["standings"].append(i)

    ctf["challenges"].append(challenges)
    with open("./ctf.json", "w") as f:
        json.dump(ctf, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
