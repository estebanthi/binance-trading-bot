import backtrader as bt
from dataclasses import field
from dataclasses import dataclass


@dataclass
class Value:
    """
    Backtrader's value observer
    Default name is "value_observer"

    """
    observer = bt.Observer = bt.observers.Value
    parameters: dict = field(default_factory=lambda:{'_name':"value_observer"})