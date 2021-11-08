from models.Strategies.BracketStratSkeleton import BracketStratSkeleton as BracketStratSkeleton
from backtrader.indicators import MACD as MACD
from backtrader.indicators import CrossOver as CrossOver
from backtrader.indicators import ExponentialMovingAverage as EMA
from dataclasses import dataclass
from models.Strategies.Strategy import Strategy as Strategy


class MACD_Crossings_strat(BracketStratSkeleton):
    params = (
        ('period_me1', 12),
        ('period_me2', 26),
        ('period_signal', 9),
        ('trend_ema_period', 100),
        ('movav', EMA),
    )

    def __init__(self):
        super().__init__()
        self.macd = MACD(period_me1=self.p.period_me1, period_me2=self.p.period_me2, period_signal=self.p.period_signal, movav=self.p.movav)
        self.ema = EMA(period=self.p.trend_ema_period)
        self.cross = CrossOver(self.macd.macd, self.macd.signal)

    def get_long(self):
        if self.ema[0] < self.datas[0].close[0] and self.cross[0] == 1:
            return True
        return False

    def get_short(self):
        if self.ema[0] > self.datas[0].close[0] and self.cross[0] == -1:
            return True
        return False


@dataclass
class MACD_Crossings(Strategy):

    def __init__(self, recurring_recap=MACD_Crossings_strat.params.recurring_recap, logging=MACD_Crossings_strat.params.logging, longs_enabled=MACD_Crossings_strat.params.longs_enabled, shorts_enabled=MACD_Crossings_strat.params.shorts_enabled,
                 stop_loss=MACD_Crossings_strat.params.stop_loss, risk_reward_ratio=MACD_Crossings_strat.params.risk_reward_ratio,
                 period_me1=MACD_Crossings_strat.params.period_me1, period_me2=MACD_Crossings_strat.params.period_me2, period_signal=MACD_Crossings_strat.params.period_signal,
                 trend_ema_period=MACD_Crossings_strat.params.trend_ema_period, movav=MACD_Crossings_strat.params.movav):
        self.strategy = MACD_Crossings_strat
        self.parameters = locals()
        self.remove_self()
