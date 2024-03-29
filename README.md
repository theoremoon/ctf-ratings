# CTF-Ratings

ctftime.org じゃないレーティングシステム考えて、ついでに色がついたら最高だよねというプロダクト


## レートとパフォーマンス

基本的にAtCoderに準拠している。

- コンテストの対象レーティングが存在しない
- 初期パフォーマンスは1200
- レーティング上限なし

## Difficulty

レートXのチームがその問題を解ける確率が50%のとき、その問題のDifficultyはX


## How to contribute?

### Add CTF Result

Add `<CTF>.json` to `./data/events/`. Scoreboard format is following mainly https://ctftime.org/json-scoreboard-feed.

```json
{
  "tasks": ["task1", "task2", ...],
  "standings": [
    {
      "pos": 1,
      "team": "teamName",
      "score": 1333,
      "taskStats": {
        "task1": {
          "points": 1,
          "time": 1615117300
        },
        "task2": {
          "points": 1,
          "time": 1615117300
        }
      }
    },
    { ... }
  ],
  "date": 1600000000, // added
  "name": "CTF Name" // added
}
```

### Add your team alias

See example https://github.com/theoremoon/ctf-ratings/blob/main/data/teams/zer0pts.json

## Missing CTFs

- D^3 CTF (scoreserver is closed)
- vishwaCTF 2021 (cloudflare protection)
- BCA CTF 2021 (no scoreserver)
- White-Hats Break the Syntax CTF (ssl handshake failed)
- Volga CTF2021 Qualifier (non-scrapable original platform)
- BSides Canberra CTF 2021 (scoreboard closed already)
- Cyber Apocalypse 2021 (how do I scrape htb ctf platform?)
- Hero CTF v3 (bot check)
- WPICTF (cloudflare)
- TAMU CTF (cannot see solved tasks of other teams)
- pwn2win (I forgot to collect the scoreboard ;_;)
- Circle City Con CTF 2021 (scoreboard closed immediately after the competition)
- THC CTF 2021 (registration closed immediately after the competition and challenges were only opened for the competitors)
- CyberThreatForce CTF | 2021 (registration is closed / scoreboard not available)
- CyBRICS CTF (I cannot know each teams solved what challenges)
- ~~RAR CTF (I cannot know each teams solved what challenges)~~ added by @willwam845 at (https://github.com/theoremoon/ctf-ratings/pull/57)
- Really Awesome CTF (ditto)
- InCTF (scoreserver is closed)
- FwordCTF 2021 (scoreserver is unstable to scrape)
- YauzaCTF 2021 (cannot see solved tasks of other teams)
- WORMCON 0x01 (UserAgent Denied)
- GrabCON (cloudflare protection)
- RCTF 2021 (XCTF)

## Author

- theoremoon (zer0pts)

## License

 Apache 2.0
