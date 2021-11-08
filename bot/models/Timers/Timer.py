import backtrader as bt


class Timer:
    """ Modelizes a timer and its params"""

    def __init__(self, name, parameters, function):
        self.timername = name
        self.parameters = parameters
        self.function = function