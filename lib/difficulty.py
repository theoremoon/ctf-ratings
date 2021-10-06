from sklearn.linear_model import LogisticRegression
from typing import List

def calc_difficulty(solve_team_perfs: List[float], unsolve_team_perfs: List[float])->float:
    """
    問題のdifficultyを推定する
    問題のdifficultyがX = performance Xのチームが50%の確率でそれを解ける
    中身はロジスティック回帰
    """

    if len(solve_team_perfs) == 0:
        return 10000

    if len(unsolve_team_perfs) == 0:
        return int(min(solve_team_perfs))

    lr = LogisticRegression()
    lr.fit([[x] for x in solve_team_perfs + unsolve_team_perfs], [1]*len(solve_team_perfs) + [0]*len(unsolve_team_perfs))

    h = 10000
    l = -10000
    while abs(h - l) > 1:
        m = (h + l) // 2
        res = lr.predict_proba([[m]])[0][0]

        if res > 0.5:
            l = m
        else:
            h = m
    return int(max(l, min(solve_team_perfs)))


