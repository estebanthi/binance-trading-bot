import backtrader as bt
import datetime as dt
from models.Strategies.StrategySkeleton import StrategySkeleton as StrategySkeleton


class BracketStratSkeleton(StrategySkeleton):
    params = (
        ('stop_loss', 0.5),
        ('risk_reward_ratio', 2),
    )

    def __init__(self):
        super().__init__()
        self.orefs = list()


    def notify_order(self, order):
        self.log('Order ref: {} / Type {} / Status {}'.format(
            order.ref, 'Buy' * order.isbuy() or 'Sell',
            order.getstatusname()))
        if not order.alive() and order.ref in self.orefs:
            self.orefs.remove(order.ref)

    def next(self):
        self.get_values()
        self.log(f"Close : {self.datas[0].close[0]}")

        if self.orefs:
            return

        if not self.position:
            if self.get_long() and self.p.longs_enabled:
                prices = self.get_prices('long')
                self.log(f'BUY BRACKET CREATE : '
                         f'\nMain : {self.datas[0].close[0]}'
                         f'\nStop : {prices[0]}'
                         f'\nTake Profit : {prices[1]}')
                os = self.buy_bracket(price=self.datas[0].close[0], stopprice=prices[0], limitprice=prices[1])
                self.orefs = [o.ref for o in os]

            if self.get_short() and self.p.shorts_enabled:
                prices = self.get_prices('short')
                self.log(f'SELL BRACKET CREATE : '
                         f'\nMain : {self.datas[0].close[0]}'
                         f'\nStop : {prices[0]}'
                         f'\nTake Profit : {prices[1]}')
                os = self.sell_bracket(price=self.datas[0].close[0], stopprice=prices[0], limitprice=prices[1])
                self.orefs = [o.ref for o in os]

    def get_prices(self, side):
        return self.get_stop_price(side), self.get_takeprofit_price(side)

    def get_stop_price(self, side):
        if side == 'long':
            stop_price = self.datas[0].close[0] * (1 - self.p.stop_loss / 100)  # Stop price is x% below actual close
        if side == 'short':
            stop_price = self.datas[0].close[0] * (1 + self.p.stop_loss / 100)  # Stop price is x% above actual close
        return stop_price

    def get_takeprofit_price(self, side):
        stop_price = self.get_stop_price(side)
        if side == 'long':
            take_profit_price = self.datas[0].close[0] + (self.datas[0].close[0] - stop_price) \
                                * self.p.risk_reward_ratio  # Take profit is function of risk reward and stop price
        if side == 'short':
            take_profit_price = self.datas[0].close[0] - (stop_price - self.datas[0].close[0]) \
                                * self.p.risk_reward_ratio
        return take_profit_price

