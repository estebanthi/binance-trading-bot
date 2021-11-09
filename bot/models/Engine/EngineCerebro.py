import backtrader as bt
from termcolor import colored


class EngineCerebro(bt.Cerebro):
    params = (
        ("mode", "BACKTEST"),
        ("telegram_bot", None)
    )

    def notify_timer(self, timer, when, *args, **kwargs):
        timername = kwargs.get("timername")

        if timername == "stop_timer":
            kwargs.get("function")(cerebro=self)

    def notify_data(self, data, status, *args, **kwargs):
        self.p.telegram_bot.send_message(f"--- DATA LOADED ---\n--- RUNNING {self.p.mode} MODE ---")
