import backtrader as bt


class High(bt.Indicator):

    lines = ("high",)

    def __next__(self):
        self.l.high[0] = self.datas[0].high[0]
