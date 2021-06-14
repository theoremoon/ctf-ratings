# CTF-Ratings

ctftime.org じゃないレーティングシステム考えて、ついでに色がついたら最高だよねというプロダクト


## レートとパフォーマンス

基本的にAtCoderに準拠している。

- コンテストの対象レーティングが存在しない
- 初期パフォーマンスは1000
- レーティング上限なし

## Difficulty

レートXのチームがその問題を解ける確率が90%のとき、その問題のDifficultyはX


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
  "date": 1600000000,
  "name": "CTF Name"
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

## Author

- theoremoon (in zer0pts)

## License

 Apache 2.0
