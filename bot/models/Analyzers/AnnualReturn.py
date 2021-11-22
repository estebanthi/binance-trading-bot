from dataclasses import dataclass
import backtrader as bt
from dataclasses import field


@dataclass
class AnnualReturn:
    analyzer: bt.analyzers.AnnualReturn = bt.analyzers.AnnualReturn
    parameters: dict = field(default_factory=lambda:{'_name':"annual_return"})