from dataclasses import dataclass
import backtrader as bt
from dataclasses import field


@dataclass
class PyFolio:
    analyzer: bt.analyzers.PyFolio = bt.analyzers.PyFolio
    parameters: dict = field(default_factory=lambda:{'_name':"py_folio"})