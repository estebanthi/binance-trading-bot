from models.Sizers.Sizer import Sizer as Sizer
import backtrader as bt
from dataclasses import dataclass
from dataclasses import field


@dataclass
class PercentSizer(Sizer):

    def __init__(self, percents=10):
        self.sizer = bt.sizers.PercentSizer
        self.parameters = {"percents": percents}

