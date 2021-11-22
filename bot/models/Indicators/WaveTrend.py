import backtrader as bt
from backtrader.indicators import ExponentialMovingAverage as EMA
from backtrader.indicators import MovingAverageSimple as SMA
from backtrader.indicators import CrossOver as CrossOver


class WaveTrend(bt.Indicator):
    """
    Wavetrend indicator
    More details on trading view
    
    """
    params = (('channel_len', 9), ('average_len', 12), ('ma_len', 3), ('os_level', 53), ('ob_level', -53))
    lines = ('wt1', 'wt2', 'cross', 'ob', 'os', 'cross_up', 'cross_down')

    def __init__(self):
        source = (self.datas[0].close + self.datas[0].high + self.datas[0].low) / 3

        esa = EMA(source, period=self.p.channel_len)
        de = EMA(abs(source - esa), period=self.p.channel_len)
        ci = (source - esa) / (0.015 * de)

        wt1 = EMA(ci, period=self.p.average_len)
        wt2 = SMA(wt1, period=self.p.ma_len)

        ob = wt2 >= self.p.ob_level
        os = wt2 <= self.p.os_level

        wtCross = CrossOver(wt1, wt2)
        cross_up = wt2 - wt1 <= 0
        cross_down = wt2 - wt1 >= 0

        self.lines.wt1 = wt1
        self.lines.wt2 = wt2
        self.lines.ob = ob
        self.lines.os = os
        self.lines.cross = wtCross
        self.lines.cross_up = cross_up
        self.lines.cross_down = cross_down
