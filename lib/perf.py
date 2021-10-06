import math
from typing import List

INITIAL_PERF = 1200.0

def avg_perf(perfs: List[float]) -> float:
    """
    get average of past perfomances
    """
    if len(perfs) == 0:
        perfs = [INITIAL_PERF]
    return sum([p*0.9**(i+1) for i, p in enumerate(reversed(perfs))]) / sum(0.9**(i+1) for i in range(len(perfs)))

def calc_performance(team_perfs: List[List[float]]) -> List[float]:
    """
    team_perfs: 参加したチームの過去のパフォーマンス。今回の順位に昇順にソートされている
    各チームの過去のパフォーマンスは時刻に昇順になっている
    """
    avg_perfs = [avg_perf(p) for p in team_perfs]
    def f(x: int) -> float:
        """
        あるチームがi位のとき、 f(x) = i - 0.5 を満たすxがそのチームのパフォーマンス
        この関数はxの値に対して単調減少する
        """
        perf = 0
        for a_perf in avg_perfs:
            perf += 1 / (1 + (6 ** ((x - a_perf) / 400)))
        return perf

    perfs = []
    # i位のチームのパフォーマンスを二分探索で求める
    for i in range(len(team_perfs)):
        l, h = -10000, 10000
        while abs(h - l) > 1:
            m = (l + h) // 2
            perf = f(m)
            if perf < (i + 1) - 0.5:
                h = m
            else:
                l = m
        perfs.append(l)
    return perfs

def calc_new_rating(past_perfs: List[float], perf: float) -> float:
    """
    past_perfs: 過去のパフォーマンス
    perf: 今回のパフォーマンス
    returns: new rating
    """
    def adjust(rating: float, n: int) -> float:
        """参加回数が少ないと正確に値が出ないので補正するらしい
        n: 参加回数
        https://github.com/kenkoooo/AtCoderProblems/blob/d4c125df495d4ebbbab507f024fccc5744768ad6/lambda-functions/time-estimator/rating.py#L25
        """
        f_1 = 1.0
        f_inf = 1 / (19 ** 0.5)
        f_n = ((1 - 0.81 ** n) ** 0.5) / ((19 ** 0.5) * (1 - 0.9 ** n))
        return rating - (f_n - f_inf) / (f_1 - f_inf) * 1200

    past_perfs.reverse()
    n = len(past_perfs) + 1
    exp_perf_sum = sum(2.0 ** (p / 800) * 0.9**(i+1) for i, p in enumerate([perf] + past_perfs))
    rating = 800 * math.log2(exp_perf_sum / sum(0.9**(i+1) for i in range(n)))
    return adjust(rating, n)

def calc_new_ahc_rating(past_perfs: List[float], perf: float) -> float:
    """
    AHCに沿ってレーティングを求める (https://www.dropbox.com/s/ne358pdixfafppm/AHC_rating.pdf?dl=0)
    past_perfs: 過去のパフォーマンス
    perf: 今回のパフォーマンス
    returns: new rating
    """
    R = 0.8271973364
    S = 724.4744301
    Q = sorted([p - S*math.log(j) for p in past_perfs + [perf] for j in range(1, 101)], reverse=True)
    numerator = sum([Q[i-1]*R**i for i in range(1, 101)])
    denominator = sum([R**i for i in range(1, 101)])
    r = numerator / denominator

    if r >= 400:
        return r
    else:
        return 400 / math.exp((400 - r) / 400.0)


