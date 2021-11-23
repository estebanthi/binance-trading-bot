# Strategies Development



## Bracket or Simple strategy ?

A bracket strategy is a strategy using stop losses and take profits. When a position is open, the only way to close it is by triggering either a stop loss or a take profit.

If you want to close a strategy using indicators or specific signals, consider using a simple strat. 



## Backtrader Strategy syntax

Once you have chosen your strategy type, you have to code the core class.



### Inheritance

First, you want your strategy class to inherit a skeleton depending on his type.

```python
class MySimpleStrat_strat(SimpleStratSkeleton):
    """
    Some code here
    """
    
class MyBracketStrat_strat(BracketStratSkeleton):
    """
    Some code here
    """
```



### Parameters

Then, you can define some parameters for your strategy. For example, in a strategy using moving averages, you can imagine the period of moving averages can vary to try different things.

You write it like the following :

```python
params = (
	("my_param_1", <default_value_1>),
    ("my_param_2", <default_value_2>),
    ...
)
```

If you only use one parameter in your strategy, don't forget the comma in the syntax so that params is considered as a tuple.

```python
params = (
	("my_param", <default_value>)  # Wrong syntax, missing comma
)

params = (
	("my_param", <default_value>),  # Better with the comma
)
```



### Init

Now, you want to define the init method containing everything you need in your logic.

You first need to call the super() constructor. And then, you can define attributes like indicators, initial values, etc...

```python
def __init__(self):
    super().__init__()
    self.ema1 = EMA(period=13)
    self.ema2 = EMA(period=self.p.ema_period)  # self.p give access to parameters you defined above
```



### Logic methods

The final step is to code logic methods.

**get_long(self)** : long trade entry signal

**get_short(self)** : long trade entry signal

Example :

```python
def get_long(self):
	if self.datas[0].close[0] > self.fast[0] > self.middle[0] > self.slow[0]:
    	return True  # Condition valid, open signal
    return False  # Else, no signal
```



#### SimpleStrat specific logic

For simple strategies, you want to specify the close position method.

**close_long(self)** : long trade close signal

**close_short(self)** : short_trade close signal



#### BracketStrat specific logic

For bracket strategies, you want to specify how are stop prices and take profits calculated. If you don't specify those methods, default will be used (stop loss is % of actual price, take profit is calculated using risk reward ratio, those values are defined in parameters)

**get_stop_price(self, side)** : stop price calculation

**get_takeprofit_price(self, side)** : take profit price calculation

Example : 

```python
def get_stop_price(self, side):
    if side == 'long':
        lows = [self.datas[0].low[i] for i in range(-self.p.pullbacks_period, 0)]
        stop_price = min(lows)
    if side == 'short':
        highs = [self.datas[0].high[i] for i in range(-self.p.pullbacks_period, 0)]
        stop_price = max(highs)
    return stop_price
```



### Some default parameters

Some parameters are present by default. You can edit their default value by redefining them in your strategy class. 

- **logging**, False : if you want to log everything happens during trading session
- **longs_enabled**, True : if you want to enable longs in your strategy
- **shorts_enabled**, True : if you want to enable shorts in your strategy
- **recurring_recap**, dt.timedelta(minutes=60) : a recap will be generated every x minutes to inform you about strategy results



#### BracketStrat specific parameters

* **stop_loss**, 0.5 : default stop loss order price in % of the open price
* **risk_reward_ratio**, 2 : default risk reward ratio



## Wrap it in a dataclass

Then, once your strategy has been developped, you want to wrap it in a dataclass to make it readable by the engine.

Here is the syntax : 

```python
@dataclass
class MyStrategy(Strategy):  # You want to make it a subclass of Strategy class

    def __init__(self, 
                 param1=MyStrategy_strat.parameters.param1,  # You define your parameters
                 param2=MyStrategy_strat.parameters.param2,
                 ...
                ):
        self.strategy = MyStrategy_strat  # Your backtrader strategy class
        self.parameters = locals()  # Do not touch it, parameters binding
        self.remove_self()  # Do not touch too

```



## Use your strategy in the Engine

Now, you can simply use your strategy in an Engine.

Example :

```python
strategies = [MyStrategy(param1=5, param2=10)]

engine_configuration = {
    # some code here
    strategies=strategies
}
```



**That's all !** Now you know how to develop a strategy for this bot. You've seen, it was easy ;)

