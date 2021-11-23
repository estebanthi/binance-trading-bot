import backtrader as bt


class Timer:
    """
    Modelizes a timer
    A timer is a function wich will be executed at a precise time in a strategy


    Parameters :

        - timername : str
            Name of the timer

        - parameters : dict
            Timer parameters

        - function : function
            Function to use

    """

    def __init__(self, name, parameters, function):
        self.timername = name
        self.parameters = parameters
        self.function = function