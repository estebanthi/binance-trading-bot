import backtrader as bt
from models.Indicators.Fractals.PriceFractals import PriceFractals as PriceFractals


class Divergences(bt.Indicator):
    """
    Generic divergences indicator


    Params :

        - bars : int
            Number of bars used for calculation, default is 2


    Output :

        - bear_div : float
            Bearish divergences

        - bull_div : float
            Bullish divergences

        - bear_div_hidden : float
            Hidden bearish divergences

        - bull_div_hidden : float
            Hidden bullish divergences

        - bars : int
            Bars parameter

    """

    params = (('bars', 2),)
    lines = ('bear_div', 'bull_div', 'bear_div_hidden', 'bull_div_hidden', 'bars')

    def __init__(self):
        self.fractals = PriceFractals(bars=self.params.bars)

    def next(self):
        self.l.bars[0] = self.p.bars
        self.l.bear_div[0] = 0
        self.l.bull_div[0] = 0
        self.l.bear_div_hidden[0] = 0
        self.l.bull_div_hidden[0] = 0

        # We find a local maxima
        if self.fractals.fractals[0] == 1:

            # We loop from the index 0 to the previous local maxima
            for i in range(-1, -len(self.datas[0].close), -1):

                if self.fractals.fractals[i] == 1:
                    # We found it, now we check if maximas have increased or decreased
                    price_increase = self.data.close[0] > self.datas[0].close[i]
                    increase = self.src[0] > self.src[i]

                    if price_increase:
                        if not increase:  # Bearish div
                            self.l.bear_div[0] = self.src[i] - self.src[0]

                    if not price_increase:
                        if increase:  # Bearish hidden divergence
                            self.l.bear_div_hidden[0] = self.src[0] - self.src[i]
                    break

        # Same thing for minimas
        if self.fractals.fractals[0] == -1:

            # We loop from the index 0 to the previous local maxima
            for i in range(-1, -len(self.datas[0].close), -1):

                if self.fractals.fractals[i] == -1:
                    # We found it, now we check if minimas have increased or decreased
                    price_decrease = self.datas[0].close[0] < self.datas[0].close[i]
                    decrease = self.src[0] < self.src[i]

                    if price_decrease:
                        if not decrease:  # RSI negative divergence
                            self.l.bull_div[0] = self.src[0] - self.src[i]

                    if not price_decrease:
                        if decrease:  # RSI divergence
                            self.l.bull_div_hidden[0] = self.src[i] - self.src[0]
                    break
