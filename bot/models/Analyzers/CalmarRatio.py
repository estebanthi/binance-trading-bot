from dataclasses import dataclass
import backtrader as bt
from dataclasses import field
from models.Analyzers.CustomReturns import CustomReturns_analyzer
from backtrader.analyzers.drawdown import DrawDown


class CalmarRatio_analyzer(bt.Analyzer):

    def __init__(self):
        self.cr = CustomReturns_analyzer()
        self.dd = DrawDown()


    def get_analysis(self):
        ann_ret = self.cr.get_analysis()["ann_ret"]
        max_dd = self.dd.get_analysis().max.drawdown
        return {"calmar_ratio": ann_ret/max_dd}


@dataclass
class CalmarRatio:
    """
    Default name is "calmar_ratio"

    """
    analyzer: CalmarRatio_analyzer = CalmarRatio_analyzer
    parameters: dict = field(default_factory=lambda: {'_name': "calmar_ratio"})
