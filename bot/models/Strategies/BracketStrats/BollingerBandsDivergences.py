from models.Strategies.BracketStratSkeleton import BracketStratSkeleton as BracketStratSkeleton
from backtrader.indicators import BollingerBands as BB
from backtrader.indicators import ExponentialMovingAverage as EMA
from models.Strategies.Strategy import Strategy as Strategy
from dataclasses import dataclass


class BollingerBandsDivergence_strat(BracketStratSkeleton):
    """
    BollingerBandsDivergence strategy
    We're looking for divergences to enter a trade

    """

    params = (
        ('bb_period', 20),
        ('devfactor', 2),
        ('trend_ema_period', 200),
    )

    def __init__(self):
        super().__init__()
        self.bb = BB(period=self.p.bb_period, devfactor=self.p.devfactor)
        self.ema200 = EMA(period=self.p.trend_ema_period)

    def get_long(self):
        if self.ema200[0] < self.datas[0].close[0] < self.bb.bot[0]:
            return True
        return False

    def get_short(self):
        if self.ema200[0] > self.datas[0].close[0] > self.bb.top[0]:
            return True
        return False


@dataclass
class BollingerBandsDivergence(Strategy):

    def __init__(self, recurring_recap=BollingerBandsDivergence_strat.params.recurring_recap, logging=BollingerBandsDivergence_strat.params.logging, longs_enabled=BollingerBandsDivergence_strat.params.longs_enabled, shorts_enabled=BollingerBandsDivergence_strat.params.shorts_enabled,
                 stop_loss=BollingerBandsDivergence_strat.params.stop_loss, risk_reward_ratio=BollingerBandsDivergence_strat.params.risk_reward_ratio,
                 bb_period=BollingerBandsDivergence_strat.params.bb_period, devfactor=BollingerBandsDivergence_strat.params.devfactor, trend_ema_period=BollingerBandsDivergence_strat.params.trend_ema_period):
        self.strategy = BollingerBandsDivergence_strat
        self.parameters = locals()
        self.remove_self()
