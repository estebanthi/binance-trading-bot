from dataclasses import dataclass
import backtrader as bt


@dataclass
class Analyzer:
    """ Modelizes an analyzer and its params"""
    analyzer: bt.Analyzer
    parameters: dict