from models.Strategies.BracketStratSkeleton import BracketStratSkeleton as BracketStratSkeleton
from models.Indicators.WaveTrend import WaveTrend as WT
from dataclasses import dataclass
from models.Strategies.Strategy import Strategy as Strategy


class Core(BracketStratSkeleton):
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

    def __init__(self, logging=Core.params.logging, longs_enabled=Core.params.longs_enabled, shorts_enabled=Core.params.shorts_enabled,
                 stop_loss=Core.params.stop_loss, risk_reward_ratio=Core.params.risk_reward_ratio,
                 channel_len_wt=Core.params.channel_len_wt, average_len_wt=Core.params.average_len_wt, ma_len_wt=Core.params.ma_len_wt,
                 os_level_wt=Core.params.os_level_wt, ob_level_wt=Core.params.ob_level_wt):
        self.strategy = Core
        self.parameters = locals()
        self.remove_self()