from sklearn.linear_model import LogisticRegression

def calc_difficulty(challenge_id, teams):
    """
    問題のdifficultyを推定する
    問題のdifficultyがX = performance Xのチームが90%の確率でそれを解ける
    AtCoder Problemsでは50%だと思うけど50%でうまく動かすのは難しかった

    中身はロジスティック回帰
    """
    perfs = [[t["performance"]] for t in teams]
    solved = [1 if int(challenge_id) in map(int, t["solves"]) else 0 for t in teams]

    if all([s == 1 for s in solved]):
        return -10000

    if all([s == 0 for s in solved]):
        return 10000

    lr = LogisticRegression()
    lr.fit(perfs, solved)

    h = 10000
    l = -10000
    while abs(h - l) > 1:
        m = (h + l) // 2
        res = lr.predict_proba([[m]])[0][0]

        if res > 0.9:
            l = m
        else:
            h = m
    return l


