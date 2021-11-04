import backtrader as bt


class SimpleStrat(bt.Strategy):
    params = (
        ('logging', False),
        ('longs_enabled', True),
        ('shorts_enabled', True),
    )

    def __init__(self):
        self.order = None

    def log(self, txt, dt=None):
        if self.params.logging:
            dt = dt or self.datas[0].datetime.datetime(0)
            print(f"{dt} : {txt}")

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

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log(f"Close, {self.datas[0].close[0]}")

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
                self.close(exectype=bt.Order.Close)
            if self.close_short() and self.position.size < 0:
                self.log('SHORT POS CLOSED, %.2f' % self.datas[0].close[0])
                self.close(exectype=bt.Order.Close)

    def get_long(self):
        return False

    def get_short(self):
        return False

    def close_long(self):
        return False

    def close_short(self):
        return False
