import argparse
import sys
import json
import os
from typing import List, Dict
from datetime import datetime
from lib.scraper import BSidesSFScraper, D3CTFScraper

PLATFORMS = {"bsidessf": BSidesSFScraper, "d3ctf": D3CTFScraper}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("date")
    parser.add_argument("url")
    parser.add_argument("--platform", default="ctfd")
    parser.add_argument("--session")
    parser.add_argument("--token")
    parser.add_argument("--mode", default="teams")

    args = parser.parse_args()
    if args.platform not in PLATFORMS:
        print("Currently supported platforms are: {}".format(PLATFORMS.keys()), file=sys.stderr)
        quit(1)

    scraper = PLATFORMS[args.platform](args.url, session=args.session, mode=args.mode, token=args.token)
    data = scraper.scoreboard()
    data["date"] = int(datetime.strptime(args.date, "%Y-%m-%d").timestamp())
    data["name"] = args.name

    with open("./data/events/{}.json".format(args.name), "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
