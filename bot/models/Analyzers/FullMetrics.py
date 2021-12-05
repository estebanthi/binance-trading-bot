from dataclasses import dataclass, field
import backtrader as bt

from models.Analyzers.CustomReturns import CustomReturns_analyzer
from models.Analyzers.ReturnsVolatility import ReturnsVolatility_analyzer
from models.Analyzers.TradesInfo import TradesInfo_analyzer
from models.Analyzers.CalmarRatio import CalmarRatio_analyzer
from backtrader.analyzers import SharpeRatio_A
from backtrader.analyzers import TradeAnalyzer
from backtrader.analyzers import DrawDown


class FullMetrics_analyzer(bt.Analyzer):

    def __init__(self):
        self.custom_returns_analyzer = CustomReturns_analyzer()
        self.ret_vol_analyzer = ReturnsVolatility_analyzer()
        self.sharpe_ratio_analyzer = SharpeRatio_A()
        self.trade_analyzer = TradeAnalyzer()
        self.dd_analyzer = DrawDown()
        self.trades_info_analyzer = TradesInfo_analyzer()
        self.calmar_analyzer = CalmarRatio_analyzer()

    def get_analysis(self):
        ann_ret = self.custom_returns_analyzer.get_analysis()["ann_ret"]

        ret_vol = self.ret_vol_analyzer.get_analysis()["volatility"]

        sharpe_ratio = self.sharpe_ratio_analyzer.get_analysis()["sharperatio"]
        calmar_ratio = self.calmar_analyzer.get_analysis()["calmar_ratio"]

        trade_analysis = self.trade_analyzer.get_analysis()

        pnlcomm = trade_analysis["pnl"]["net"]["total"]
        pnl = trade_analysis["pnl"]["gross"]["total"]
        fees = pnl - pnlcomm

        open_trades_nb = trade_analysis.total.open
        close_trades_nb = trade_analysis.total.closed
        close_shorts_nb = trade_analysis.short.total
        close_longs_nb = trade_analysis.long.total

        avg_return = self.trades_info_analyzer.get_analysis()["avg_return"]
        avg_return_short = self.trades_info_analyzer.get_analysis()["avg_return_short"]
        avg_return_long = self.trades_info_analyzer.get_analysis()["avg_return_long"]

        winrate = trade_analysis.won.total / close_trades_nb

        len_in_market = trade_analysis.len.total
        average_trade_len = trade_analysis.len.average
        longest_trade_len = trade_analysis.len.max
        average_won_len = trade_analysis.len.won.average
        average_lost_len = trade_analysis.len.lost.average

        drawdown_analysis = self.dd_analyzer.get_analysis()
        average_drawdown = drawdown_analysis["drawdown"]
        average_drawdown_length = drawdown_analysis["len"]
        max_drawdown = drawdown_analysis["max"]["drawdown"]
        max_drawdown_length = drawdown_analysis["max"]["len"]

        return {
            "Annual returns": ann_ret,
            "PNL net": pnlcomm,
            "Fees": fees,
            "Winrate": winrate,
            "Total trades": close_trades_nb,
            "Total long": close_longs_nb,
            "Total short": close_shorts_nb,
            "Open trades": open_trades_nb,
            "Average return per trade": avg_return,
            "Average return per long": avg_return_long,
            "Average return per short": avg_return_short,
            "Time in market": len_in_market,
            "Average trade len": average_trade_len,
            "Max trade len": longest_trade_len,
            "Average won len": average_won_len,
            "Average lost len": average_lost_len,
            "Average drawdown": average_drawdown,
            "Average drawdown length": average_drawdown_length,
            "Max drawdown": max_drawdown,
            "Max drawdown length": max_drawdown_length,
            "Annualized Sharpe ratio": sharpe_ratio,
            "Calmar ratio": calmar_ratio,
            "Returns volatility": ret_vol,
        }


@dataclass
class FullMetrics:
    """
    FullMetrics analyzer.
    Default name is "custom_returns"

    """
    analyzer: FullMetrics_analyzer = FullMetrics_analyzer
    parameters: dict = field(default_factory=lambda: {'_name': "full_metrics"})
