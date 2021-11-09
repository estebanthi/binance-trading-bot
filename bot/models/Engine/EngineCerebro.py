import backtrader as bt
from termcolor import colored
import datetime as dt


class EngineCerebro(bt.Cerebro):
    params = (
        ("mode", "BACKTEST"),
        ("telegram_bot", None),
        ("symbol", None),
        ("path_to_result", None)
    )

    def notify_timer(self, timer, when, *args, **kwargs):
        timername = kwargs.get("timername")

        if timername == "stop_timer":
            kwargs.get("function")(cerebro=self)

    def notify_data(self, data, status, *args, **kwargs):
        self.p.telegram_bot.send_message(f"--- DATA LOADED ---\n--- RUNNING {self.p.mode} MODE ---\n--- SYMBOL {self.p.symbol} ---")
        self.p.telegram_bot.send_message(f"From {self.datas[0].p.fromdate.strftime('%m/%d/%Y, %H:%M:%S')}")

