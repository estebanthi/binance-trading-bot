from enum import Enum
from dataclasses import dataclass

import backtrader as bt
from backtrader.indicators import ExponentialMovingAverage



indicators = [

]

class Types(Enum):
    PRICE_COMPARABLE = 1
    SELF_COMPARABLE = 2


@dataclass
class Indicator:
    name: str
    core: bt.Indicator
    parameters: list = None
    flags: list = None
