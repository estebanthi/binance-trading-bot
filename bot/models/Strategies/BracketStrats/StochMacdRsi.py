from models.Strategies.BracketStratSkeleton import BracketStratSkeleton as BracketStratSkeleton
from backtrader.indicators import MACD as MACD
from backtrader.indicators import CrossOver as CrossOver
from backtrader.indicators import Stochastic as Stochastic
from backtrader.indicators import RelativeStrengthIndex as RSI
from backtrader.indicators import ExponentialMovingAverage as EMA
from backtrader.indicators import SmoothedMovingAverage as SMA
from backtrader.indicators import MovingAverageSimple as MAS
from models.Indicators.Fractals.PriceFractals import PriceFractals as PriceFractals
from dataclasses import dataclass
from models.Strategies.Strategy import Strategy as Strategy


class StochMacdRsi_strat(BracketStratSkeleton):
    params = (
        ('period_me1', 12),
        ('period_me2', 26),
        ('period_signal', 9),
        ('movav_macd', EMA),
        ('period_rsi', 14),
        ('movav_rsi', SMA),
        ('period_stoch', 14),
        ('period_dfast', 3),
        ('period_dslow', 3),
        ('movav_stoch', MAS),
        ('upperband_stoch', 80),
        ('lowerband_stoch', 20),
        ('stop_loss_limit', 5),
    )

    def __init__(self):
        super().__init__()
        self.macd = MACD(period_me1=self.p.period_me1, period_me2=self.p.period_me2, period_signal=self.p.period_signal,
                         movav=self.p.movav_macd)
        self.cross = CrossOver(self.macd.macd, self.macd.signal)
        self.rsi = RSI(period=self.p.period_rsi, movav=self.p.movav_rsi)
        self.stoch = Stochastic(period=self.p.period_stoch, period_dfast=self.p.period_dfast,
                                period_dslow=self.p.period_dslow, movav=self.p.movav_stoch,
                                upperband=self.p.upperband_stoch, lowerband=self.p.lowerband_stoch)
        self.fractals = PriceFractals().fractals_signal
        info = self.broker.getcommissioninfo(self.datas[0])

    def get_long(self):
        if self.rsi[0] > 50 and self.previous_stoch_oversell > self.previous_stoch_overbought \
                and self.previous_macd_cross_up > self.previous_stoch_overbought:
            return True
        return False

    def get_short(self):
        if self.rsi[0] < 50 and self.previous_stoch_overbought > self.previous_stoch_oversell \
                and self.previous_macd_cross_down > self.previous_stoch_overbought:
            return True
        return False

    def get_previous_stoch_overbought(self):
        index = 0
        while self.stoch.percK[index] < self.p.upperband_stoch and self.stoch.percD[index] < self.p.upperband_stoch:
            index -= 1
        return index

    def get_previous_stoch_oversell(self):
        index = 0
        while self.stoch.percK[index] > self.p.lowerband_stoch or self.stoch.percD[index] > self.p.lowerband_stoch:
            index -= 1
        return index

    def get_previous_macd_cross_up(self):
        index = 0
        while self.cross[index] != 1 and index > -len(self.cross):
            index -= 1
        return index

    def get_previous_macd_cross_down(self):
        index = 0
        while self.cross[index] != -1 and index > -len(self.cross):
            index -= 1
        return index

    def get_previous_swing_high(self):
        index = 0
        while self.fractals[index] != 1 and index > -len(self.fractals):
            index -= 1
        return self.datas[0].close[index]

    def get_previous_swing_low(self):
        index = 0
        while self.fractals[index] != -1 and index > -len(self.fractals):
            index -= 1
        return self.datas[0].close[index]

    def get_values(self):
        self.previous_stoch_overbought = self.get_previous_stoch_overbought()
        self.previous_stoch_oversell = self.get_previous_stoch_oversell()
        self.previous_macd_cross_up = self.get_previous_macd_cross_up()
        self.previous_macd_cross_down = self.get_previous_macd_cross_down()

    def get_stop_price(self, side):
        if side == 'long':
            previous_swing_low = self.get_previous_swing_low()
            limit = self.datas[0].close[0] * (1 - self.p.stop_loss_limit / 100)
            return previous_swing_low if previous_swing_low > limit else limit
        if side == 'short':
            previous_swing_high = self.get_previous_swing_high()
            limit = self.datas[0].close[0] * (1 + self.p.stop_loss_limit / 100)
            return previous_swing_high if previous_swing_high < limit else limit


@dataclass
class StochMacdRsi(Strategy):

    def __init__(self, recurring_recap=StochMacdRsi_strat.params.recurring_recap, logging=StochMacdRsi_strat.params.logging, longs_enabled=StochMacdRsi_strat.params.longs_enabled, shorts_enabled=StochMacdRsi_strat.params.shorts_enabled,
                 stop_loss=StochMacdRsi_strat.params.stop_loss, risk_reward_ratio=StochMacdRsi_strat.params.risk_reward_ratio,
                 period_me1=StochMacdRsi_strat.params.period_me1, period_me2=StochMacdRsi_strat.params.period_me2, period_signal=StochMacdRsi_strat.params.period_signal,
                 movav_macd=StochMacdRsi_strat.params.movav_macd, period_rsi=StochMacdRsi_strat.params.period_rsi, movav_rsi=StochMacdRsi_strat.params.movav_rsi,
                 period_stoch=StochMacdRsi_strat.params.period_stoch, period_dfast=StochMacdRsi_strat.params.period_dfast, period_dslow=StochMacdRsi_strat.params.period_dslow,
                 movav_stoch=StochMacdRsi_strat.params.movav_stoch, upperband_stoch=StochMacdRsi_strat.params.upperband_stoch, lowerband_stoch=StochMacdRsi_strat.params.lowerband_stoch,
                 stop_loss_limit=StochMacdRsi_strat.params.stop_loss_limit):
        self.strategy = StochMacdRsi_strat
        self.parameters = locals()
        self.remove_self()