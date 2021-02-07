import math
from typing import List, Dict

class PerfomanceCalculator():
    def __init__(self, teams: Dict[str, Dict]):
        self.teams = teams

    def get_past_perfs(self, team: str) -> List[float]:
        if team not in self.teams:
            return [1000.0] # initial performance of each team

        return [e["performance"] for e in self.teams[team]["events"].values()]

    def get_perticipant_times(self, team: str) -> int:
        """
        teamの出場回数を返す
        """
        if team not in self.teams:
            return 0

        return len(self.get_past_perfs(team))

    def get_avg_perf(self, team: str) -> float:
        """
        get average of past perfomances
        note: AtCoder式では新しいパフォーマンスを優先しているが、こちらはそうしないので加重平均ではなく単なる平均をとっている
        """
        perfs = self.get_past_perfs(team)
        return sum(perfs) / len(perfs)

    def calc_performance(self, teams: List[str]) -> List[float]:
        """
        teams: 順位に昇順にソートされている
        https://qiita.com/anqooqie/items/92005e337a0d2569bdbd#%E5%86%85%E9%83%A8%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%B3%E3%82%B9%E3%81%AE%E7%AE%97%E5%87%BA
        """
        avg_perfs = [self.get_avg_perf(t) for t in teams]
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
        for i in range(len(teams)):
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

    def calc_new_rating(self, team: str, perf: float) -> float:
        """
        team: チーム名
        perf: 今回のパフォーマンス
        returns: new rating

        note: 新しいコンテストの結果を重視と、初心者への慈悲を導入してない
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

        n = self.get_perticipant_times(team) + 1
        exp_perf_sum = sum(2.0 ** (p / 800) for p in self.get_past_perfs(team) + [perf])
        rating = 800 * math.log2(exp_perf_sum / n)
        return adjust(rating, n)

