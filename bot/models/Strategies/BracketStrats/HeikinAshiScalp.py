from models.Strategies.BracketStratSkeleton import BracketStratSkeleton as BracketStratSkeleton
from models.Indicators.HeikinAshiRSI import HeikinAshiRSI
from backtrader.indicators import ExponentialMovingAverage as EMA
from models.Strategies.Strategy import Strategy as Strategy
from dataclasses import dataclass
import backtrader as bt
from models.Indicators.Fractals.PriceFractals import PriceFractals


class HeikinAshiScalp_strat(BracketStratSkeleton):
    """
    BollingerBandsDivergence strategy
    We're looking for divergences to enter a trade

    """

    params = (
        ('period', 14),
        ('smoothing', 7),
    )

    def __init__(self):
        super().__init__()
        self.ema200 = EMA(period=200)
        self.ha = HeikinAshiRSI(period=self.p.period, smoothing=self.p.smoothing)
        self.fractals = PriceFractals(bars=3)

    def get_long(self):
        if self.ema200[0] < self.datas[0].close[0]:
            last_pullback = self.find_last_pullback()
            if self.datas[0].close[0] > self.datas[0].close[-1] and last_pullback < -5:
                return True
        return False

    def get_short(self):
        if self.ema200[0] > self.datas[0].close[0]:
            last_pullback = self.find_last_pullback()
            if self.datas[0].close[0] < self.datas[0].close[-1] and last_pullback < -5:
                return True
        return False

    def get_stop_price(self, side):
        if side == "long":
            index = self.find_last_swing_low()
            return self.datas[0].low[index]
        if side == "short":
            index = self.find_last_swing_high()
            return self.datas[0].high[index]

    def find_last_swing_low(self):
        index = 0
        while self.fractals.fractals_signal[index] != -1:
            index -= 1
        return index

    def find_last_swing_high(self):
        index = 0
        while self.fractals.fractals_signal[index] != 1:
            index -= 1
        return index

    def find_last_pullback(self):
        index = 0
        while self.ha.high[index] < 0 or self.ha.low[index] > 0:
            index -= 1
        return index

@dataclass
class HeikinAshiScalp(Strategy):

    def __init__(self, recurring_recap=HeikinAshiScalp_strat.params.recurring_recap,
                 logging=HeikinAshiScalp_strat.params.logging, longs_enabled=HeikinAshiScalp_strat.params.longs_enabled,
                 shorts_enabled=HeikinAshiScalp_strat.params.shorts_enabled,
                 stop_loss=HeikinAshiScalp_strat.params.stop_loss,
                 risk_reward_ratio=HeikinAshiScalp_strat.params.risk_reward_ratio,
                 period=HeikinAshiScalp_strat.params.period, smoothing=HeikinAshiScalp_strat.params.smoothing):
        self.strategy = HeikinAshiScalp_strat
        self.parameters = locals()
        self.remove_self()
