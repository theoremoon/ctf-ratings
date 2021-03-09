# CTF-Ratings

ctftime.org じゃないレーティングシステム考えて、ついでに色がついたら最高だよねというプロダクト


## レートとパフォーマンス

基本的にAtCoderに準拠している。

- Unratedが存在しない
- NoSub撤退がない
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

## Author

- theoremoon (in zer0pts)

## License

 Apache 2.0
