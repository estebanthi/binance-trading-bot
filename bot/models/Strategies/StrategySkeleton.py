import backtrader as bt
from termcolor import colored
import datetime as dt
from backtrader.utils import AutoOrderedDict
from termcolor import colored


class StrategySkeleton(bt.Strategy):
    """ Modelizes a strategy skeleton """
    params = (  # Universal params
        ('logging', False),
        ('longs_enabled', True),
        ('shorts_enabled', True),
        ('recurring_recap', dt.timedelta(minutes=60)),
    )

    def __init__(self):
        # Telegram notif
        self.notify_beginning_telegram()

        self.total_profit = 0

        self.add_timer(when=bt.timer.SESSION_START, offset=self.p.recurring_recap, repeat=self.p.recurring_recap,
                       timername="recurring_recap")

    def notify_data(self, data, status, *args, **kwargs):
        self.status = data._getstatusname(status)
        if status == data.LIVE:
            self.log("LIVE DATA - Ready to trade")
        else:
            print(dt.datetime.now().strftime("%d-%m-%y %H:%M"), "NOT LIVE - %s" % self.status)

    def log(self, txt, dt=None):
        """ Logging method """
        if self.params.logging:
            dt = dt or self.datas[0].datetime.datetime(0)
            print(f"{dt} : {txt}")

    def notify_trade(self, trade):
        """ Enabled everytime a trade is finished """
        if not trade.isclosed:
            return
        color = "green" if trade.pnlcomm > 0 else "red"
        self.log(colored('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                         (trade.pnl, trade.pnlcomm), color))
        self.total_profit += trade.pnlcomm
        color = "green" if self.total_profit > 0 else "red"
        self.log(colored("TOTAL PROFIT : %.2f" % self.total_profit, color))

    """ Generic strategies methods """

    def get_long(self):
        return False

    def get_short(self):
        return False

    def close_long(self):
        return False

    def close_short(self):
        return False

    def get_values(self):
        return

    def notify_timer(self, timer, when, **kwargs):
        timername = kwargs.get("timername", None)

        if timername == "recurring_recap" and self.cerebro.p.mode != "BACKTEST":
            if "trade_analyzer" in dir(self.analyzers):
                analysis_result = self.analyzers.trade_analyzer.get_analysis()
                self.format_recap(analysis_result)
                self.notify_recap(analysis_result)

    def notify_recap(self, analysis):
        self.cerebro.p.telegram_bot.send_message(colored("------- RECURRING RECAP -------", "cyan"))
        for k1, v1 in analysis.items():
            if type(v1) == AutoOrderedDict:
                for k2, v2 in v1.items():
                    if type(v2) == AutoOrderedDict:
                        for k3, v3 in v2.items():
                            if type(v3) == AutoOrderedDict:
                                for k4, v4 in v3.items():
                                    self.cerebro.p.telegram_bot.send_message(f"{k1}/{k2}/{k3}/{k4} : {v4}")
                            else:
                                self.cerebro.p.telegram_bot.send_message(f"{k1}/{k2}/{k3} : {v3}")
                    else:
                        self.cerebro.p.telegram_bot.send_message(f"{k1}/{k2} : {v2}")
            else:
                self.cerebro.p.telegram_bot.send_message(f"{k1} : {v1}")
        self.cerebro.p.telegram_bot.send_message(colored("------- END -------", "cyan"))

    def format_recap(self, analysis):
        print(colored("------- RECURRING RECAP -------", "cyan"))
        for k1, v1 in analysis.items():
            if type(v1) == AutoOrderedDict:
                for k2, v2 in v1.items():
                    if type(v2) == AutoOrderedDict:
                        for k3, v3 in v2.items():
                            if type(v3) == AutoOrderedDict:
                                for k4, v4 in v3.items():
                                    print(f"{k1}/{k2}/{k3}/{k4} : {v4}")
                            else:
                                print(f"{k1}/{k2}/{k3} : {v3}")
                    else:
                        print(f"{k1}/{k2} : {v2}")
            else:
                print(f"{k1} : {v1}")
        print(colored("------- END -------", "cyan"))

    def notify_beginning_telegram(self):
        if self.cerebro.p.mode == "BACKTEST":
            self.cerebro.p.telegram_bot.send_message(
                f"--- DATA LOADED ---\n--- RUNNING {self.cerebro.p.mode} MODE ---\n--- SYMBOL {self.cerebro.p.symbol} ---")

    def stop(self):
        if "trade_analyzer" in dir(self.analyzers):
            analysis_result = self.analyzers.trade_analyzer.get_analysis()
            self.format_recap(analysis_result)