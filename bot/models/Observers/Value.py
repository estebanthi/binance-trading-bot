import backtrader as bt
from models.Observers.Observer import Observer as Observer
from dataclasses import field
from dataclasses import dataclass


@dataclass
class Value:
    observer = bt.Observer = bt.observers.Value
    parameters: dict = field(default_factory=lambda:{'_name':"value_observer"})