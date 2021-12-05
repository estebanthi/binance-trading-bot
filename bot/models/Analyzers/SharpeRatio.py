from dataclasses import dataclass
import backtrader as bt
from dataclasses import field


@dataclass
class SharpeRatio:
    """
    Trade analyzer from backtrader
    Default name is "sharpe_ratio"

    """
    analyzer: bt.analyzers.SharpeRatio_A = bt.analyzers.SharpeRatio_A
    parameters: dict = field(default_factory=lambda: {'_name': "sharpe_ratio"})
