import backtrader as bt
from termcolor import colored


class StrategySkeleton(bt.Strategy):
    """ Modelizes a strategy skeleton """
    params = (  # Universal params
        ('logging', False),
        ('longs_enabled', True),
        ('shorts_enabled', True),
    )

    def log(self, txt, dt=None):
        """ Logging method """
        if self.params.logging:
            dt = dt or self.datas[0].datetime.datetime(0)
            print(f"{dt} : {txt}")

    def notify_trade(self, trade):
        """ Enabled everytime a trade is finished """
        if not trade.isclosed:
            return
        color = None
        if trade.pnl > 0:
            color = "green"
        else:
            color = "red"
        self.log(colored('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm), color))

    """ Generic strategies methods """
    def get_long(self):
        return False
    def get_short(self):
        return False
    def close_long(self):
        return False
    def close_short(self):
        return False
