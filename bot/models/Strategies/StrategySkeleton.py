import backtrader as bt
from termcolor import colored
import datetime as dt


class StrategySkeleton(bt.Strategy):
    """ Modelizes a strategy skeleton """
    params = (  # Universal params
        ('logging', False),
        ('longs_enabled', True),
        ('shorts_enabled', True),
    )

    def __init__(self):
        self.total_profit = 0

    def notify_data(self, data, status, *args, **kwargs):
        self.status = data._getstatusname(status)
        if status == data.LIVE:
            self.log("LIVE DATA - Ready to trade")
        else:
            print(dt.datetime.now().strftime("%d-%m-%y %H:%M"), "NOT LIVE - %s" % self.status)

    def log(self, txt, dt=None):
        """ Logging method """
        if self.params.logging:
            dt = dt or self.datas[0].datetime.datetime(0)
            print(f"{dt} : {txt}")

    def notify_trade(self, trade):
        """ Enabled everytime a trade is finished """
        if not trade.isclosed:
            return
        color = "green" if trade.pnlcomm > 0 else "red"
        self.log(colored('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm), color))
        self.total_profit += trade.pnlcomm
        color = "green" if self.total_profit > 0 else "red"
        self.log(colored("TOTAL PROFIT : %.2f" % self.total_profit, color))

    """ Generic strategies methods """
    def get_long(self):
        return False
    def get_short(self):
        return False
    def close_long(self):
        return False
    def close_short(self):
        return False
    def get_values(self):
        return
