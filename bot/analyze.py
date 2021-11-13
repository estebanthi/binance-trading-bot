# Imports
from models.Analyzers.ResultAnalyzer import ResultAnalyzer as ResultAnalyzer
from models.ResultsLoader import ResultsLoader as ResultsLoader

loader = ResultsLoader()
results = loader.load("results.dat")

analyzer = ResultAnalyzer(results)
print(analyzer.get_pnls())

