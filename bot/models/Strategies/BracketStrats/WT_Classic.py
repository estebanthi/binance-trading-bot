from models.Strategies.BracketStratSkeleton import BracketStratSkeleton as BracketStratSkeleton
from models.Indicators.WaveTrend import WaveTrend as WT
from dataclasses import dataclass
from models.Strategies.Strategy import Strategy as Strategy


class WT_Classic_strat(BracketStratSkeleton):
    params = (
        ('channel_len_wt', 9),
        ('average_len_wt', 12),
        ('ma_len_wt', 3),
        ('os_level_wt', 53),
        ('ob_level_wt', -53),
    )

    def __init__(self):
        super().__init__()
        self.wt = WT(channel_len=self.p.channel_len_wt, average_len=self.p.average_len_wt, ma_len=self.p.ma_len_wt,
                     os_level=self.p.os_level_wt, ob_level=self.p.ob_level_wt)

    def get_long(self):
        if self.wt.cross_up[0] == 1 and self.wt.cross != 0 and self.wt.os:
            return True
        return False

    def get_short(self):
        if self.wt.cross_down[0] == 1 and self.wt.cross != 0 and self.wt.ob:
            return True
        return False

@dataclass
class WT_Classic(Strategy):

    def __init__(self, recurring_recap=WT_Classic_strat.params.recurring_recap, logging=WT_Classic_strat.params.logging, longs_enabled=WT_Classic_strat.params.longs_enabled, shorts_enabled=WT_Classic_strat.params.shorts_enabled,
                 stop_loss=WT_Classic_strat.params.stop_loss, risk_reward_ratio=WT_Classic_strat.params.risk_reward_ratio,
                 channel_len_wt=WT_Classic_strat.params.channel_len_wt, average_len_wt=WT_Classic_strat.params.average_len_wt, ma_len_wt=WT_Classic_strat.params.ma_len_wt,
                 os_level_wt=WT_Classic_strat.params.os_level_wt, ob_level_wt=WT_Classic_strat.params.ob_level_wt):
        self.strategy = WT_Classic_strat
        self.parameters = locals()
        self.remove_self()