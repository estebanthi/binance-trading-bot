from models.Strategies.BracketStratSkeleton import BracketStratSkeleton as BracketStratSkeleton
from backtrader.indicators import ParabolicSAR as PSAR
from backtrader.indicators import ExponentialMovingAverage as EMA
from dataclasses import dataclass
from models.Strategies.Strategy import Strategy as Strategy


class PSAR_EMA_strat(BracketStratSkeleton):
    params = (
        ("psar_period", 2),
        ("psar_af", 0.02),
        ("psar_afmax", 0.2),
        ("trend_ema_period", 200),
        ("risk_reward_ratio", 1.5),
    )

    def __init__(self):
        super().__init__()
        self.psar = PSAR(period=self.p.psar_period, af=self.p.psar_af, afmax=self.p.psar_afmax)
        self.ema = EMA(period=self.p.trend_ema_period)

    def get_long(self):
        if self.ema[0] < self.datas[0].close[0] and self.psar[0] < self.datas[0].close[0]:
            return True
        return False

    def get_short(self):
        if self.ema[0] > self.datas[0].close[0] and self.psar[0] > self.datas[0].close[0]:
            return True
        return False

    def get_stop_price(self, side):
        return self.psar[0]


@dataclass
class PSAR_EMA(Strategy):

    def __init__(self, recurring_recap=PSAR_EMA_strat.params.recurring_recap,
                 logging=PSAR_EMA_strat.params.logging, longs_enabled=PSAR_EMA_strat.params.longs_enabled,
                 shorts_enabled=PSAR_EMA_strat.params.shorts_enabled,
                 risk_reward_ratio=PSAR_EMA_strat.params.risk_reward_ratio,
                 psar_period=PSAR_EMA_strat.params.psar_period,
                 psar_af=PSAR_EMA_strat.params.psar_af,
                 psar_afmax=PSAR_EMA_strat.params.psar_afmax,
                 trend_ema_period=PSAR_EMA_strat.params.trend_ema_period):
        self.strategy = PSAR_EMA_strat
        self.parameters = locals()
        self.remove_self()
