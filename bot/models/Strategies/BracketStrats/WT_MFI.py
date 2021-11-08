from models.Strategies.BracketStratSkeleton import BracketStratSkeleton as BracketStratSkeleton
from backtrader.indicators import ExponentialMovingAverage as EMA
from models.Indicators.WaveTrend import WaveTrend as WT
from models.Indicators.MFI import MFI as MFI
from models.Indicators.Pullbacks import Pullbacks as Pullbacks
from dataclasses import dataclass
from models.Strategies.Strategy import Strategy as Strategy


class WT_MFI_strat(BracketStratSkeleton):
    params = (
        ('pullbacks_period', 10),
    )

    def __init__(self):
        super().__init__()
        self.ema50 = EMA(period=50)
        self.ema200 = EMA(period=200)
        self.wt = WT()
        self.mfi = MFI()
        self.pullbacks = Pullbacks(ema_period=50)

    def get_long(self):
        if self.wt.cross[0] == 1 and self.datas[0].close > self.ema200[0] and self.mfi[0] > 0 \
                and self.wt.wt1 < 0 and self.wt.wt2 < 0 and 1 in self.find_pullbacks():
            return True
        return False

    def get_short(self):
        if self.wt.cross[0] == -1 and self.datas[0].close < self.ema200[0] and self.mfi[0] < 0 \
                and self.wt.wt1 > 0 and self.wt.wt2 > 0 and -1 in self.find_pullbacks():
            return True
        return False

    def find_pullbacks(self):
        pullbacks_list = [self.pullbacks[i] for i in range(-self.p.pullbacks_period, 0)]
        return pullbacks_list

    def get_stop_price(self, side):
        if side == 'long':
            lows = [self.datas[0].low[i] for i in range(-self.p.pullbacks_period, 0)]
            stop_price = min(lows)
        if side == 'short':
            highs = [self.datas[0].high[i] for i in range(-self.p.pullbacks_period, 0)]
            stop_price = max(highs)
        return stop_price


@dataclass
class WT_MFI(Strategy):

    def __init__(self, recurring_recap=WT_MFI_strat.params.recurring_recap, logging=WT_MFI_strat.params.logging, longs_enabled=WT_MFI_strat.params.longs_enabled,
                 shorts_enabled=WT_MFI_strat.params.shorts_enabled,
                 stop_loss=WT_MFI_strat.params.stop_loss, risk_reward_ratio=WT_MFI_strat.params.risk_reward_ratio,
                 pullbacks_period=WT_MFI_strat.params.pullbacks_period):
        self.strategy = WT_MFI_strat
        self.parameters = locals()
        self.remove_self()
