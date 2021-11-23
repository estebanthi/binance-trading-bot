[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Basic Overview

Using crypto historical data, backtest your strategies, optimize the parameters and analyze the results. Once you found a promising strategy, automatically trade with it in live using Binance API. Be notified on Telegram about what's happening within the bot.



## Visualize the results

![](https://zupimages.net/up/21/45/dnis.png)



## Key features

* **Develop** trading components easily :
  * Strategies : to decide whether to enter / exit a trade or not.
  * Indicators : to give information about data to your strategies.
  * Analyzers : to analyze the results of your backtests or trading sessions.
  * Sizers : to define how much quantity of assets the engine should buy depending on parameters.
  * Observers : to define what you plot on the results chart.
  * Timers : to define actions to do at a precise time, repeatedly or not.
* **Backtest** and **optimize** your strategies to find the best parameters.
* **Visualize** the results on a chart you can configure.
* Automatic **live trading** with fake or real money, using Binance API. 
* **Telegram notifications** when the bot does specific actions (entering a trade, loading data, ...)
* **MongoDB support** if you don't want to store data locally.



## How to install

```
# clone the repo
git clone https://github.com/estebanthi/BinanceTradingBotV4

# go to folder
cd BinanceTradingBotV4/bot

# install requirements
pip3 install -r requirements.txt
pip3 install git+git://github.com/Dave-Vallance/bt-ccxt-store
```

Go into `backtrader` package, in folder `plot`, open file `locator.py`, and remove warnings in line 35, because it is deprecated :

```python
from matplotlib.dates import (HOURS_PER_DAY, MIN_PER_HOUR, SEC_PER_MIN,
                              MONTHS_PER_YEAR, DAYS_PER_WEEK,
                              SEC_PER_HOUR, SEC_PER_DAY,
                              num2date, rrulewrapper, YearLocator,
                              MicrosecondLocator, warnings) # Remove warnings here
```



## How to use

To use the bot, just go in the folder ```bot``` and create your first run script, or edit the one already existing. But first, you have to create the ```config.yml``` file.



### Create and configure the config file

First, create a ```config.yml``` in the `bot` file. Fill it like the following :

```yaml
api_key: "<YOUR BINANCE API KEY>"
api_secret: "<YOUR BINANCE API SECRET>"

telegram_token: "<YOUR TELEGRAM BOT TOKEN>" # If you want to use Telegram
user: "<YOUR TELEGRAM USER ID>"

mongo_url: "<YOUR MONGO DATABASE URL>" # If you want to use MongoDB for storing data
```

If you don't know how to use Binance API, you can check it on https://www.binance.com/en-NG/support/faq/360002502072.

If you don't know how to get a Telegram token, you can check it on https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot.



### Setting up your trading components

First, you need to decide what you want to use with the engine. So, for example, you can set up your components like that :

```python
# (you can use multiple strategies at the same time for backtesting or live trading)
strategies = [TripleEMA(logging=True), MACD_Crossings(period_me1=12)]
sizer = DefaultSizer() # you can use only one sizer (it's logic !)
analyzers = [TradeAnalyzer(), Returns()]
observers = [ValueObserver()]
timers = [StopSession(when=dt.time(0), weekdays=[7])]
```



### Use additional features

You can use some more features, like a writer to write details about your session into a file, or a TelegramBot to be notified on Telegram.

```python
telegram_bot = TelegramBot()
write_to = "results.txt"
```



### Set up your engine configuration

```python
config = EngineConfiguration(
	mode="BACKTEST", # Chose between BACKTEST, OPTIMIZE, PAPER or LIVE
    symbol="BTC/EUR", # What you want to trade
    start_date="2021/01/01 00:00:00", # Session start date (format YYYY/MM/DD HH:MM:SS)
    end_date=dt.datetime.now(), # Session end
    timedelta=dt.timedelta(days=100), # Can replace start date because it will be calculated using this end_date - timedelta
    timeframe=bt.TimeFrame.Days, # Timeframe
    compression=1, # Timeframe * compression = resolution
    strategies=strategies,
    analyzers=analyzers,
    sizer=sizer,
    observers=observers,
    timers=timers,
    cash=100_000, # Virtual cash for the broker
    commission=0.2 # 0.2% broker commission 
    currency="EUR" # What you use to live trade
    telegram_bot=telegram_bot, # If you want to use Telegram
    write_to=write_to, # If you want to save results file
    debug=True, # If you want to debug the datafeed
    stdstats=True, # For default chart plotting
)
```



### Run the engine

When you have your config, you can just run your engine.

```python
engine = Engine() # Instantiate the engine
engine.set_configuration(config) # Set the config
result = engine.run() # Get the results
engine.plot() # Display the chart

# If you use a telegram bot, you can send the results to your Telegram
telegram_bot.send_file(open(f"data/backtesting_results/{write_to}", "r")) 
```



## Develop !

If you want to use the bot the best way, you will have to develop  strategies, indicators, analyzers, ... First, you have to understand the ```backtrader``` python library, because everything operates around this. Find the documentation here : https://www.backtrader.com/docu/.

I will add the documentation later for more details...



## Notes

#### Raspberry PI

For backtesting, it's better to have a strong processor, but for live trading, a nice implementation for this trading bot is on Raspberry PI, so that it can runs 24/7. 

#### Multiple timeframes

Be careful when using multiple strategies with multiple timeframes, because it can cause some issues. Check the code for more details.



## To Do

- [x] Document the code
- [x] Rename strategies
- [x] Add Telegram notifications
- [x] Add some development documentation
- [ ] Modify some indicators plotlines
- [ ] Add MongoDB results support

