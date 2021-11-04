import backtrader as bt
from dataclasses import dataclass


@dataclass
class Sizer:
    """ Modelizes a sizer """
    sizer: bt.Sizer
    parameters: dict