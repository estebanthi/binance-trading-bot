from models.Sizers.Sizer import Sizer as Sizer
import backtrader as bt
from dataclasses import dataclass


@dataclass
class FixedSizer(Sizer):

    def __init__(self, stake=1):
        self.sizer = bt.sizers.FixedSize
        self.parameters = {"stake": stake}

