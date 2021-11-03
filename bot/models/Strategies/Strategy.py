from dataclasses import dataclass
import backtrader as bt


@dataclass
class Strategy:
    """ Modelizes a strategy and its params"""
    strategy: bt.Strategy
    parameters: dict