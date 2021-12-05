from dataclasses import dataclass, field
import backtrader as bt

from models.Analyzers.CustomReturns import CustomReturns_analyzer
from models.Analyzers.ReturnsVolatility import ReturnsVolatility_analyzer
from backtrader.analyzers import SharpeRatio_A
from backtrader.analyzers import TradeAnalyzer


class FullMetrics_analyzer(bt.Analyzer):

    def __init__(self):
        self.custom_returns_analyzer = CustomReturns_analyzer()
        self.ret_vol_analyzer = ReturnsVolatility_analyzer()
        self.sharpe_ratio_analyzer = SharpeRatio_A()
        self.trade_analyzer = TradeAnalyzer()

    def get_analysis(self):
        ann_ret = self.custom_returns_analyzer.get_analysis()["ann_ret"]
        ret_vol = self.ret_vol_analyzer.get_analysis()["volatility"]
        sharpe_ratio = self.sharpe_ratio_analyzer.get_analysis()["sharperatio"]

        trade_analysis = self.trade_analyzer.get_analysis()
        pnlcomm = trade_analysis["pnl"]["net"]["total"]
        pnl = trade_analysis["pnl"]["gross"]["total"]
        fees = pnl - pnlcomm


        return {"Annual returns": ann_ret, "Returns volatility": ret_vol, "Annualized Sharpe ratio": sharpe_ratio,
                "PNL net": pnlcomm, "Fees": fees}


@dataclass
class FullMetrics:
    """
    FullMetrics analyzer.
    Default name is "custom_returns"

    """
    analyzer: FullMetrics_analyzer = FullMetrics_analyzer
    parameters: dict = field(default_factory=lambda: {'_name': "full_metrics"})
