from dataclasses import dataclass
import backtrader as bt


@dataclass
class Strategy:
    strategy: bt.Strategy
    parameters: dict

    def remove_self(self):
        del self.parameters["self"]


