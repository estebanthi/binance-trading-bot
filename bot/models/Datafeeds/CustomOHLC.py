import backtrader.feeds as btfeed


class CustomOHLC(btfeed.GenericCSVData):
    """
    A generic CSV class corresponding to extracted data from the bot

    """

    # Columns mapping
    params = (
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1)
    )