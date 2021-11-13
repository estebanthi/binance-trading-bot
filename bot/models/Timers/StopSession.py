import backtrader as bt
import datetime as dt
from models.Timers.Timer import Timer as Timer
from termcolor import colored


def stop_run(cerebro):
    if cerebro.p.telegram_bot:
        cerebro.p.telegram_bot.send_message("SESSION FINISHED")
    cerebro.runstop()


class StopSession(Timer):

    def __init__(self, when=dt.time(hour=0), weekdays=[]):
        super().__init__("stop_timer", {"when": when, "weekdays": weekdays}, stop_run)
