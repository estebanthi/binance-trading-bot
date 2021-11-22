import pymongo
import yaml
import datetime as dt


class MongoDriver:

    def __init__(self):
        self.client = None

    def connect(self):
        with open("config.yml", "r") as file:
            url = yaml.safe_load(file)["mongo_url"]
        client = pymongo.MongoClient(url)
        if client:
            print("MongoDriver connected")
        self.client = client

    def add_ticker(self, ticker, timeframe, historical):
        db = self.client.tradingbot
        collection = db.Tickers
        collection.insert_one({"symbol": ticker, "timeframe": timeframe, "historical": historical})

    def update_ticker(self, ticker, timeframe, historical):
        db = self.client.tradingbot
        collection = db.Tickers

        collection.update({"symbol": "BTC/EUR"}, {"$set": {"historical": historical}})

    def get_historical(self, ticker, timeframe):
        db = self.client.tradingbot
        collection = db.Tickers

        return collection.find_one({"symbol": ticker, "timeframe": timeframe})["historical"]

    def get_ticker(self, ticker, timeframe):
        db = self.client.tradingbot
        collection = db.Tickers

        return collection.find_one({"symbol": ticker, "timeframe": timeframe})

    def close(self):
        self.client.close()
        print("MongoDriver disconnected")
