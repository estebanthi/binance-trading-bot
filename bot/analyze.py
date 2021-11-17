# Imports
from models.Analyzers.ResultAnalyzer import ResultAnalyzer as ResultAnalyzer
from models.ResultsLoader import ResultsLoader as ResultsLoader
from models.Strategies.BracketStrats.PSAR_EMA import PSAR_EMA as PSAR_EMA

loader = ResultsLoader()
results = loader.load("psar_ema_optimized_4h.dat")

analyzer = ResultAnalyzer(results)
print(analyzer.get_pnls())

