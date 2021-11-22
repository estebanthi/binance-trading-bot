import backtrader as bt
from backtrader.indicators import MovingAverageSimple as SMA
import pandas as pd
import numpy as np


class MFI(bt.Indicator):
    """
    MFI indicator


    Params :

        - period : int
            SMA period used for calculation, default is 60

        - multiplier : int
            Multiplier used for calculation, default is 150

        - yshift : float
            Yshift used for calculation, default is 2.5


    Outputs :

        - MFI : float
            MFI

        - side : int
            MFI's side

    """
    params = (('period', 60), ('multiplier', 150), ('yshift', 2.5))
    lines = ('MFI', 'side')

    def __init__(self):
        candle_data = (self.datas[0].close - self.datas[0].open) / (
                    self.datas[0].high - self.datas[0].low) * self.params.multiplier - self.params.yshift
        self.lines.MFI = SMA(candle_data, period=self.params.period)

    def next(self):
        self.lines.side[0] = 1 if self.l.MFI > 0 else -1
