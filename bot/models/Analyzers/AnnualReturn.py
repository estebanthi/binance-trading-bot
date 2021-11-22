from dataclasses import dataclass
import backtrader as bt
from dataclasses import field


@dataclass
class AnnualReturn:
    """
    Annual return analyzer from backtrader
    Default name is "annual_return"

    """
    analyzer: bt.analyzers.AnnualReturn = bt.analyzers.AnnualReturn
    parameters: dict = field(default_factory=lambda:{'_name':"annual_return"})