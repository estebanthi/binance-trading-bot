from dataclasses import dataclass
import backtrader as bt
from dataclasses import field


@dataclass
class PyFolio:
    """
    PyFolio analyzer from backtrader
    Default name is "py_folio"

    """
    analyzer: bt.analyzers.PyFolio = bt.analyzers.PyFolio
    parameters: dict = field(default_factory=lambda:{'_name':"py_folio"})