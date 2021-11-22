import backtrader as bt
from backtrader.indicators import ExponentialMovingAverage as EMA


class Pullbacks(bt.Indicator):
    """
    An indicator to detect pullbacks to EMA


    Params :

        - ema_period : int
            EMA period, default is 50

        - period : int
            Period for pullbacks calculation, default is 3


    Outputs :

        - pullbacks : int
            1 if upwards pullback, -1 if downwards, else 0

    """

    params = (('ema_period', 50),('period',3))

    lines = ('pullbacks',)

    def __init__(self):

        self.high = self.datas[0].high
        self.low = self.datas[0].low
        self.ema = EMA(self.datas[0], period = self.p.ema_period)

    def next(self):
        under, above = 0, 0
        for i in range(-self.p.period, 0):
            if self.high[i] < self.ema[i]:
                under += 1
            if self.low[i] > self.ema[i]:
                above += 1

        if under == self.p.period and self.high[0] > self.ema[0]:
            self.l.pullbacks[0] = -1
        elif above == self.p.period and self.low[0] < self.ema[0]:
            self.l.pullbacks[0] = 1
        else:
            self.l.pullbacks[0] = 0