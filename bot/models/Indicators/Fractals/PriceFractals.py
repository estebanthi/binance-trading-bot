# -*- coding: utf-8 -*-

from models.Indicators.Fractals.Fractals import Fractals as Fractals


class PriceFractals(Fractals):

    def __init__(self):
        self.src = self.datas[0].close
        super().__init__()
