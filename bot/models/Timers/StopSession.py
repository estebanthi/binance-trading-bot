import datetime as dt
from models.Timers.Timer import Timer as Timer


def stop_run(cerebro):
    if cerebro.p.telegram_bot:
        cerebro.p.telegram_bot.send_message("SESSION FINISHED")
    cerebro.runstop()


class StopSession(Timer):
    """
    StopSession timer, to automatically stop the trading session at a precise time


    Parameters :

        - when : time.time
            When to stop

        - weekdays : list[str]
            List of weekdays the timer have to be enabled

    """

    def __init__(self, when=dt.time(hour=0), weekdays=[]):
        super().__init__("stop_timer", {"when": when, "weekdays": weekdays}, stop_run)
