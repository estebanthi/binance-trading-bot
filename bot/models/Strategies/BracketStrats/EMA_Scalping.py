from models.Strategies.BracketStratSkeleton import BracketStratSkeleton as BracketStratSkeleton
from backtrader.indicators import CrossOver
from backtrader.indicators import ExponentialMovingAverage as EMA
from models.Strategies.Strategy import Strategy as Strategy
from dataclasses import dataclass
import backtrader as bt


class EMA_Scalping_strat(BracketStratSkeleton):
    """
    BollingerBandsDivergence strategy
    We're looking for divergences to enter a trade

    """

    params = (
        ('slow_period', 200),
        ('fast_period', 50),
    )

    class CandlePos(bt.Indicator):
        lines = ("pos",)
        params = (
            ("period", 50),
        )

        def __init__(self):
            self.ema = EMA(period=self.p.period)

        def next(self):
            if self.datas[0].low[0] > self.ema[0]:
                self.l.pos[0] = 1
            elif self.datas[0].high[0] < self.ema[0]:
                self.l.pos[0] = -1
            else:
                self.l.pos[0] = 0

    def __init__(self):
        super().__init__()
        self.slow_ema = EMA(period=self.p.slow_period)
        self.fast_ema = EMA(period=self.p.fast_period)
        self.crossover = CrossOver(self.fast_ema, self.slow_ema)
        self.candle_pos = self.CandlePos(period=self.p.fast_period)

        self.last_crossover = 0
        self.has_met_first_hit = False
        self.candles_since_first_hit = 0

    def get_values(self):
        if self.crossover[0] in [1, -1]:
            self.last_crossover = self.crossover[0]
            self.reset()
        if not self.has_met_first_hit:
            if self.candle_pos[-1] == 0 or self.candle_pos[-2] != self.candle_pos[-1]:
                self.has_met_first_hit = True
        if self.has_met_first_hit:
            crossover = self.last_crossover
            if crossover == 1:
                if self.candle_pos[0] < 1:
                    self.candles_since_first_hit += 1
            if crossover == -1:
                if self.candle_pos[0] > -1:
                    self.candles_since_first_hit += 1

    def reset(self):
        self.has_met_first_hit = False
        self.candles_since_first_hit = 0

    def get_long(self):
        if self.fast_ema[0] > self.slow_ema[0] \
                and self.has_met_first_hit \
                and self.candles_since_first_hit <= 3 \
                and self.datas[0].close[0] > self.datas[0].close[-1] > self.datas[0].close[-2] \
                and self.candle_pos[0] > -1:
            return True
        return False

    def get_short(self):
        if self.fast_ema[0] < self.slow_ema[0] \
                and self.has_met_first_hit \
                and self.candles_since_first_hit <= 3 \
                and self.datas[0].close[0] < self.datas[0].close[-1] < self.datas[0].close[-2] \
                and self.candle_pos[0] < 1:
            return True
        return False


@dataclass
class EMA_Scalping(Strategy):

    def __init__(self, recurring_recap=EMA_Scalping_strat.params.recurring_recap,
                 logging=EMA_Scalping_strat.params.logging, longs_enabled=EMA_Scalping_strat.params.longs_enabled,
                 shorts_enabled=EMA_Scalping_strat.params.shorts_enabled,
                 stop_loss=EMA_Scalping_strat.params.stop_loss,
                 risk_reward_ratio=EMA_Scalping_strat.params.risk_reward_ratio,
                 slow_period=EMA_Scalping_strat.params.slow_period, fast_period=EMA_Scalping_strat.params.fast_period):
        self.strategy = EMA_Scalping_strat
        self.parameters = locals()
        self.remove_self()
