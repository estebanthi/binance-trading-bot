# -*- coding: utf-8 -*-

from models.Indicators.Fractals.Fractals import Fractals as Fractals
from backtrader.indicators import RelativeStrengthIndex as RSI


class RSI_Fractals(Fractals):
    """
    Fractals for the RSI


    Params :

        - period : int
            RSI's period, default is 13
    """

    params = (
        ('period', 13),
    )

    def __init__(self):
        self.src = RSI(period=self.p.period)
        super().__init__()
