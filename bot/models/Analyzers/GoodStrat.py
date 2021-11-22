from dataclasses import dataclass
import backtrader as bt
from dataclasses import field
from models.Analyzers.CustomReturns import CustomReturns_analyzer


class GoodStrat_analyzer(bt.Analyzer):

    def __init__(self):
        self.rets = CustomReturns_analyzer()

    def get_analysis(self):
        return self.rets.get_analysis()

@dataclass
class GoodStrat:
    analyzer: GoodStrat_analyzer = GoodStrat_analyzer
    parameters: dict = field(default_factory=lambda: {'_name': "good_strat"})