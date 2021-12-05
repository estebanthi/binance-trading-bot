import backtrader as bt
from dataclasses import dataclass, field
import math
import statistics


class ReturnsVolatility_analyzer(bt.Analyzer):

    def __init__(self):
        self.returns = []

    def notify_trade(self, trade):
        if trade.isclosed:
            brokervalue = self.strategy.broker.getvalue()

            pnl = trade.history[len(trade.history) - 1].status.pnlcomm
            pnlpcnt = 100 * pnl / brokervalue

            self.returns.append(pnlpcnt)

    def get_analysis(self):

        return {"volatility": math.sqrt(statistics.variance(self.returns))}


@dataclass
class ReturnsVolatility:
    """
    Analyze returns volatility

    """
    analyzer: ReturnsVolatility_analyzer = ReturnsVolatility_analyzer
    parameters: dict = field(default_factory=lambda: {'_name': "returns_volatility"})
