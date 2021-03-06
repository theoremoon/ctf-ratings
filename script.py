import argparse
import sys
import json
from datetime import datetime

from lib.scraper.bsidessf import BSidesSFScraper
from lib.scraper.d3ctf import D3CTFScraper
from lib.scraper.ctfd_legacy import LegacyCTFdScraper
from lib.scraper.ctfd import CTFdScraper
from lib.scraper.ctfx import CTFxScraper
from lib.scraper.angstromctf import AngstromCTFScraper
from lib.scraper.midnightsun import MidnightsunScraper
from lib.scraper.plaidctf import PlaidCTFScraper
from lib.scraper.asisctf import AsisCTFScraper

PLATFORMS = {"bsidessf": BSidesSFScraper, "d3ctf": D3CTFScraper, "ctfd-legacy": LegacyCTFdScraper, "ctfd": CTFdScraper, "ctfx": CTFxScraper, "angstrom": AngstromCTFScraper, "midnightsun": MidnightsunScraper, "plaidctf": PlaidCTFScraper, "asis": AsisCTFScraper}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("date")
    parser.add_argument("url")
    parser.add_argument("--platform", default="ctfd")
    parser.add_argument("--session")
    parser.add_argument("--cookies")
    parser.add_argument("--token")
    parser.add_argument("--mode", default="teams")

    args = parser.parse_args()
    if args.platform not in PLATFORMS:
        print("Currently supported platforms are: {}".format(PLATFORMS.keys()), file=sys.stderr)
        quit(1)

    scraper = PLATFORMS[args.platform](args.url, session=args.session, mode=args.mode, token=args.token, cookies=args.cookies)
    data = scraper.scoreboard()
    data["date"] = int(datetime.strptime(args.date, "%Y-%m-%d").timestamp())
    data["name"] = args.name

    with open("./data/events/{}.json".format(args.name), "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
