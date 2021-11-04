import backtrader as bt
from models.Strategies.StrategySkeleton import StrategySkeleton as StrategySkeleton


class SimpleStratSkeleton(StrategySkeleton):
    """ Modelizes a simple strategy without stop loss or take profit """

    def __init__(self):
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))


        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        self.log(f"Close, {self.datas[0].close[0]}")
        print(self.position.size)

        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.get_long() and self.p.longs_enabled:
                self.log('BUY CREATE, %.2f' % self.datas[0].close[0])
                self.order = self.buy()

            if self.get_short() and self.p.shorts_enabled:
                self.log('SELL CREATE, %.2f' % self.datas[0].close[0])
                self.order = self.sell()



        else:
            if self.close_long() and self.position.size > 0:
                self.log('LONG POS CLOSED, %.2f' % self.datas[0].close[0])
                self.close()
            if self.close_short() and self.position.size < 0:
                self.log('SHORT POS CLOSED, %.2f' % self.datas[0].close[0])
                self.close()
