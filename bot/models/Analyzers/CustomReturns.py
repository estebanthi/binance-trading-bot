from dataclasses import dataclass
from dataclasses import field
import backtrader as bt
import math


class CustomReturns_analyzer(bt.TimeFrameAnalyzerBase):
    """
    Return analyzer, with some modifications
    """

    timeframes_mapper = {
        bt.TimeFrame.Minutes: 1,
        bt.TimeFrame.Days: 1440  # 1440 minutes in one day
    }

    def __init__(self):
        self._value_start = self.strategy.broker.getvalue()
        self._tcount = 0  # Bars counter

    def stop(self):
        self._value_end = self.strategy.broker.getvalue()

        self.rtot = (self._value_end / self._value_start - 1) * 100   # Total returns calculation
        self.avg_ret = self.rtot / self._tcount                 # Average returns calculation

        self.ann_ret = 525_600 / (self.timeframes_mapper[self.timeframe] * self.compression) * self.avg_ret  # Annualization
        self.log_ret = math.log(abs(self.ann_ret) / 100) * 100  # Log returns calculation

    def get_analysis(self):
        """
        - rtot : Total returns over period
        - ann_ret : Annualized returns
        - log_ret : Logarithmic returns

        """
        return {
            "rtot": self.rtot,
            "ann_ret": self.ann_ret,
            "log_ret": self.log_ret
        }

    def _on_dt_over(self):
        self._tcount += 1  # Counter incrementing for each iteration


@dataclass
class CustomReturns:
    """
    CustomReturns analyzer.
    Default name is "custom_returns"

    """
    analyzer: CustomReturns_analyzer = CustomReturns_analyzer
    parameters: dict = field(default_factory=lambda: {'_name': "custom_returns"})
