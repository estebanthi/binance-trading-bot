# Imports
from models.Analyzers.ResultAnalyzer import ResultAnalyzer as ResultAnalyzer
from models.ResultsLoader import ResultsLoader as ResultsLoader
from models.Strategies.BracketStrats.PSAR_EMA import PSAR_EMA as PSAR_EMA
from models.Strategies.SimpleStrats import TripleEMA

loader = ResultsLoader()
results = loader.load("triple_ema_scalping.dat")

analyzer = ResultAnalyzer(results)
print(analyzer.get_pnls())

