import backtrader as bt
from backtrader.indicators import RelativeStrengthIndex as RSI
from models.Indicators.Divergences.Divergences import Divergences as Divergences


class RSI_Divergences(Divergences):
    """
    RSI divergences


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
