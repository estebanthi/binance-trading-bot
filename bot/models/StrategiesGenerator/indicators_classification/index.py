from enum import Enum
from dataclasses import dataclass
from dataclasses import field

import backtrader as bt

from backtrader.indicators import ExponentialMovingAverage
import models.Indicators.Prices.High
import models.Indicators.Fractals.PriceFractals


class Flags(Enum):  # Flags to describe indicator's category
    PRICE_COMPARABLE = 1
    SELF_COMPARABLE = 2
    UNIQUE_VALUES = 3


@dataclass
class Indicator:  # Indicator default dataclass
    name: str
    core: bt.Indicator
    parameters: dict = field(default_factory=dict)
    flags: list = field(default_factory=list)
    values: list = field(default_factory=list)


@dataclass
class EMA(Indicator):
    def __init__(self):
        super().__init__(
            name="EMA",
            core=ExponentialMovingAverage,
            parameters={
                "period": range(5, 100, 5)
            },
            flags=[
                Flags.PRICE_COMPARABLE,
                Flags.SELF_COMPARABLE,
            ])


@dataclass
class High(Indicator):
    def __init__(self):
        super().__init__(
            name="High",
            core=models.Indicators.Prices.High.High,
        )


@dataclass
class PriceFractals(Indicator):
    def __init__(self):
        super().__init__(
            name="PriceFractals",
            core=models.Indicators.Fractals.PriceFractals.PriceFractals,
            parameters={
                "bars": range(2, 5)
            },
            flags=[
                Flags.UNIQUE_VALUES,
            ],
            values=[
                -1, 0, 1
            ]
        )


indicators = [
    EMA(), PriceFractals()
]

price_indicators = [
    High(),
]
