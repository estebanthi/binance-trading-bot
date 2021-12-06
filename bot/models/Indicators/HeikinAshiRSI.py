import backtrader as bt
from backtrader.indicators import RelativeStrengthIndex as RSI, HeikinAshi
import numpy as np

class HeikinAshiRSI(bt.Indicator):
    params = (
        ("period", 14), ("smoothing", 7)
    )

    lines = (
        "open", "high", "low", "close",
    )

    def __init__(self):
        self.zrsi_close = z_RSI(src=self.data.close, period=self.p.period)
        self.zrsi_high = z_RSI(src=self.data.high, period=self.p.period)
        self.zrsi_low = z_RSI(src=self.data.low, period=self.p.period)

    def next(self):
        zrsi_close = self.zrsi_close[0]
        zrsi_open = self.zrsi_close[0] if np.isnan(self.zrsi_close[-1]) else self.zrsi_close[-1]
        zrsi_high = self.zrsi_high[0]
        zrsi_low = self.zrsi_low[0]

        close_ = (zrsi_close + zrsi_open + zrsi_high + zrsi_low) / 4

        if np.isnan((self.zrsi_close[-1] * self.p.smoothing \
                     + (self.zrsi_close[-1] + self.zrsi_low[-1] + self.zrsi_high[-1] + self.zrsi_close[-2]) / 4 \
                     ) / (self.p.smoothing + 1)):
            open_ = (zrsi_open + zrsi_close) / 2
        else:
            open_ = (self.zrsi_close[-1] * self.p.smoothing \
                     + (self.zrsi_close[-1] + self.zrsi_low[-1] + self.zrsi_high[-1] + self.zrsi_close[-2]) / 4 \
                     ) / (self.p.smoothing + 1)
        high_ = max(zrsi_high, max(open_, close_))
        low_ = min(zrsi_low, min(open_, close_))
        self.l.open[0], self.l.high[0], self.l.low[0], self.l.close[0] = open_, high_, low_, close_


class z_RSI(bt.Indicator):
    params = (
        ("period", 7),
        ("src", None)
    )

    lines = (
        "rsi",
    )

    def __init__(self):
        self.rsi = RSI(self.p.src, period=self.p.period)

    def next(self):
        self.l.rsi[0] = self.rsi[0] - 50
