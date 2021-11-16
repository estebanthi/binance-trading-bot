# Imports
from models.Analyzers.ResultAnalyzer import ResultAnalyzer as ResultAnalyzer
from models.ResultsLoader import ResultsLoader as ResultsLoader

loader = ResultsLoader()
results = loader.load("triple_ema_optimized_4h.dat")

analyzer = ResultAnalyzer(results)
print(analyzer.get_pnls())

