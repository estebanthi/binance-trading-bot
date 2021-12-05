# Imports
from models.Results.ResultsAnalyzer import ResultsAnalyzer
from models.Results.ResultsLoader import ResultsLoader
from models.Strategies.BracketStrats.PSAR_EMA import PSAR_EMA as PSAR_EMA
from models.Strategies.SimpleStrats import TripleEMA
from models.Strategies.BracketStrats import BollingerBandsDivergences

loader = ResultsLoader()
results = loader.load("multistrat.dat")

analyzer = ResultsAnalyzer(results)
analyzer.pretty_pnls()
