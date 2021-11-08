from dataclasses import dataclass
import backtrader as bt


@dataclass
class Observer:
    """ Modelizes an observer and its params"""
    observer: bt.Observer
    parameters: dict