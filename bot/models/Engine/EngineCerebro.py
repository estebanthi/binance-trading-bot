import backtrader as bt
from termcolor import colored


class EngineCerebro(bt.Cerebro):
    params = (
        ("mode", "BACKTEST"),
    )

    def notify_timer(self, timer, when, *args, **kwargs):
        timername = kwargs.get("timername")

        if timername == "stop_timer":
            kwargs.get("function")(cerebro=self)
