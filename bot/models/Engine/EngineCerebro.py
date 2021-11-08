import backtrader as bt


class EngineCerebro(bt.Cerebro):

    params = (
        ("mode", "BACKTEST"),
    )