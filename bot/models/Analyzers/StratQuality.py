from dataclasses import dataclass
import backtrader as bt
from dataclasses import field
from models.Analyzers.CustomReturns import CustomReturns_analyzer
from backtrader.analyzers import DrawDown
from backtrader.analyzers import SharpeRatio
import math


class StratQuality_analyzer(bt.Analyzer):

    params = (
        ("acceptable_drawdown", 30),
        ("aimed_annual_returns", 50)
    )

    def __init__(self):
        self.rets = CustomReturns_analyzer()
        self.drdwn = DrawDown()
        self.sharpe = SharpeRatio()

    def get_analysis(self):
        rets_analysis = self.rets.get_analysis()
        annual_returns = rets_analysis["ann_ret"]
        log_annual_returns = rets_analysis["log_ret"]
        ret_score = sigmoid((annual_returns - self.p.aimed_annual_returns), 0.01)

        drdwn_analysis = self.drdwn.get_analysis()
        max_drawdown = drdwn_analysis["max"]["drawdown"]
        drwdn_score = sigmoid(self.p.acceptable_drawdown - max_drawdown, 0.1)

        sharpe_ratio = self.sharpe.get_analysis()["sharperatio"]
        sharpe_score = math.log(1+sharpe_ratio/1.5)



        return {
            "annual_returns": annual_returns,
            "log_annual_returns": log_annual_returns,
            "max_drawdown": max_drawdown,
            "sharpe_ratio":  sharpe_ratio,
            "quality": ret_score+drwdn_score+sharpe_score
        }


def sigmoid(x, alpha=1):
    return 1 / (1 + math.exp(-x*alpha))

@dataclass
class StratQuality:
    analyzer: StratQuality_analyzer = StratQuality_analyzer
    parameters: dict = field(default_factory=lambda: {'_name': "strat_quality"})