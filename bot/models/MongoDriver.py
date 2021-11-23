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
