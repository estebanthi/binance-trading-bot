import pickle
import yaml
from models.MongoDriver import MongoDriver


class ResultsLoader:
    """
    Useful for loading results

    If it generates errors, add strategies in imports

    """

    def __init__(self):
        self.default_path = f"data/backtesting_results/"

    def load(self, filename="results.dat", use_mongo=True):
        with open("config.yml", "r") as file:
            data = yaml.safe_load(file)
        if data["mongo_url"] and use_mongo:  # If MongoDB is used
            mongo_driver = MongoDriver()
            mongo_driver.connect()
            return pickle.loads(mongo_driver.get_result(filename)['object'])
        with open(self.default_path + filename, "rb") as file:
            return pickle.load(file)
