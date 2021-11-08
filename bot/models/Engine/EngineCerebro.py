import backtrader as bt


class EngineCerebro(bt.Cerebro):

    params = (
        ("mode", "BACKTEST"),
    )

    def notify_timer(self, timer, when, *args, **kwargs):
        print("timer")