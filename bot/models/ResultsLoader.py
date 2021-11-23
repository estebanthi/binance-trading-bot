import pickle


class ResultsLoader:
    """
    Useful for loading results

    If it generates errors, add strategies in imports

    """

    def __init__(self):
        self.default_path = f"data/backtesting_results/"

    def load(self, filename = "results.dat"):
        with open(self.default_path + filename, "rb") as file:
            return pickle.load(file)


