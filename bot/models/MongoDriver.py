import pymongo
import yaml


class MongoDriver:
    """
    Class to interact with MongoDB database

    You have to configure it in config.yml file
    Check README for more details

    """

    def __init__(self):
        self.client = None

    def connect(self):
        """
        Connect to database

        """

        with open("config.yml", "r") as file:
            url = yaml.safe_load(file)["mongo_url"]
        client = pymongo.MongoClient(url)
        if client:
            print("MongoDriver connected")
        self.client = client

    def add_ticker(self, ticker, timeframe, historical):
        """
        Add a ticker to database

        """

        db = self.client.tradingbot
        collection = db.Tickers
        collection.insert_one({"symbol": ticker, "timeframe": timeframe, "historical": historical})

    def update_ticker(self, ticker, timeframe, historical):
        """
        Update a ticker in database

        """

        db = self.client.tradingbot
        collection = db.Tickers

        collection.update({"symbol": ticker, "timeframe": timeframe}, {"$set": {"historical": historical}})

    def get_historical(self, ticker, timeframe):
        """
        Get an historical from database

        """

        db = self.client.tradingbot
        collection = db.Tickers

        return collection.find_one({"symbol": ticker, "timeframe": timeframe})["historical"]

    def get_ticker(self, ticker, timeframe):
        """
        Get a ticker from database

        """

        db = self.client.tradingbot
        collection = db.Tickers

        return collection.find_one({"symbol": ticker, "timeframe": timeframe})

    def close(self):
        """
        Close connection

        """
        self.client.close()
        print("MongoDriver disconnected")

    def add_result(self, result_name, object):
        """
        Add result object to db
        """

        db = self.client.tradingbot
        collection = db.Results
        collection.insert_one({"name": result_name, "object": object})

    def get_result(self, result_name):
        """
        Get a result object from his name

        """

        db = self.client.tradingbot
        collection = db.Results

        return collection.find_one({"name": result_name})

    def update_result(self, result_name, object):
        """
        Update a result object

        """

        db = self.client.tradingbot
        collection = db.Results

        collection.update({"name": result_name}, {"$set": {"object": object}})
