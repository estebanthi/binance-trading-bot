# -*- coding: utf-8 -*-

import backtrader as bt


class Fractals(bt.Indicator):
    """
    Fractals indicator default class


    Params :

        - bars : int
            Number of bars for fractals calculation, default is 2


    Outputs :

        - fractals : int
            1 if high fractal, -1 if low fractal, 0 else

        - fractals_signals : int
            Same as fractals, but with an offset to represent reality

    """
    
    lines = ('fractals','fractals_signal')
    params = (('bars', 2),)
    
    def next(self):
        counter = []
        for i in range(-self.p.bars, self.p.bars+1):
            if i == 0: pass
            try:
                if self.src[i] < self.src[0]:
                    counter.append(1)
                elif self.src[i] > self.src[0]:
                    counter.append(-1)
                else:
                    counter.append(0)
            except IndexError:
                break

        counter2 = []
        for i in range(-self.p.bars * 2, 1):
            try:
                if self.src[i] < self.src[-self.p.bars]:
                    counter2.append(1)
                elif self.src[i] > self.src[-self.p.bars]:
                    counter2.append(-1)
                else:
                    counter2.append(0)
            except IndexError:
                break

        if counter.count(1) == self.p.bars*2:
            self.l.fractals[0] = 1
        elif counter.count(-1) == self.p.bars*2:
            self.l.fractals[0] = -1
        else:
            self.l.fractals[0] = 0

        if counter2.count(1) == self.p.bars*2:
            self.l.fractals_signal[0] = 1
        elif counter2.count(-1) == self.p.bars*2:
            self.l.fractals_signal[0] = -1
        else:
            self.l.fractals_signal[0] = 0


