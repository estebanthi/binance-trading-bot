from dataclasses import dataclass
import backtrader as bt
from dataclasses import field


@dataclass
class TradeAnalyzer:
    """
    Trade analyzer from backtrader
    Default name is "trade_analyzer"

    """
    analyzer: bt.analyzers.TradeAnalyzer = bt.analyzers.TradeAnalyzer
    parameters: dict = field(default_factory=lambda:{'_name':"trade_analyzer"})