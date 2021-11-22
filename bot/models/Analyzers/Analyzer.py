from dataclasses import dataclass
import backtrader as bt


@dataclass
class Analyzer:
    """
    Modelizes an analyzer

    - Attributes :
        - analyzer (bt.Analyzer)
        - parameters (dict)

    """
    analyzer: bt.Analyzer
    parameters: dict