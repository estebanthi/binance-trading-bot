from dataclasses import dataclass
import backtrader as bt


@dataclass
class Observer:
    """
    Modelizes an observer

    """
    observer: bt.Observer
    parameters: dict