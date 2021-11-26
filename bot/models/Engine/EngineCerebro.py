import tqdm
import tqdm.contrib.itertools
import tqdm.auto
import itertools
from itertools import tee
import multiprocessing

import backtrader as bt
from backtrader.utils.py3 import (map)

from backtrader import linebuffer
from backtrader import indicator
from backtrader.writer import WriterFile
from backtrader.strategy import Strategy, SignalStrategy


class EngineCerebro(bt.Cerebro):
    """
    The custom cerebro used by the bot
    The cerebro is like the brain


    Params :

        - mode : str
            Cerebro's mode, default is "BACKTEST"

        - telegram_bot : TelegramBot
            TelegramBot instance, default is None

        - symbol : str
            Symbol, default is None

    """

    params = (
        ("mode", "BACKTEST"),
        ("telegram_bot", None),
        ("symbol", None),
    )

    def notify_timer(self, timer, when, *args, **kwargs):
        timername = kwargs.get("timername")
        if timername == "stop_timer":
            kwargs.get("function")(cerebro=self)

    def notify_data(self, data, status, *args, **kwargs):
        if status == data.LIVE:
            if self.p.telegram_bot:
                self.p.telegram_bot.send_message(
                    f"--- DATA LOADED ---\n--- RUNNING {self.p.mode} MODE ---\n--- SYMBOL {self.p.symbol} ---")
                self.p.telegram_bot.send_message(f"From {self.datas[0].p.fromdate.strftime('%m/%d/%Y, %H:%M:%S')}")

    def run(self, **kwargs):
        """The core method to perform backtesting. Any ``kwargs`` passed to it
        will affect the value of the standard parameters ``Cerebro`` was
        instantiated with.

        If ``cerebro`` has not datas the method will immediately bail out.

        It has different return values:

          - For No Optimization: a list contanining instances of the Strategy
            classes added with ``addstrategy``

          - For Optimization: a list of lists which contain instances of the
            Strategy classes added with ``addstrategy``
        """
        self._event_stop = False  # Stop is requested

        if not self.datas:
            return []  # nothing can be run

        pkeys = self.params._getkeys()
        for key, val in kwargs.items():
            if key in pkeys:
                setattr(self.params, key, val)

        # Manage activate/deactivate object cache
        linebuffer.LineActions.cleancache()  # clean cache
        indicator.Indicator.cleancache()  # clean cache

        linebuffer.LineActions.usecache(self.p.objcache)
        indicator.Indicator.usecache(self.p.objcache)

        self._dorunonce = self.p.runonce
        self._dopreload = self.p.preload
        self._exactbars = int(self.p.exactbars)

        if self._exactbars:
            self._dorunonce = False  # something is saving memory, no runonce
            self._dopreload = self._dopreload and self._exactbars < 1

        self._doreplay = self._doreplay or any(x.replaying for x in self.datas)
        if self._doreplay:
            # preloading is not supported with replay. full timeframe bars
            # are constructed in realtime
            self._dopreload = False

        if self._dolive or self.p.live:
            # in this case both preload and runonce must be off
            self._dorunonce = False
            self._dopreload = False

        self.runwriters = list()

        # Add the system default writer if requested
        if self.p.writer is True:
            wr = WriterFile()
            self.runwriters.append(wr)

        # Instantiate any other writers
        for wrcls, wrargs, wrkwargs in self.writers:
            wr = wrcls(*wrargs, **wrkwargs)
            self.runwriters.append(wr)

        # Write down if any writer wants the full csv output
        self.writers_csv = any(map(lambda x: x.p.csv, self.runwriters))

        self.runstrats = list()

        if self.signals:  # allow processing of signals
            signalst, sargs, skwargs = self._signal_strat
            if signalst is None:
                # Try to see if the 1st regular strategy is a signal strategy
                try:
                    signalst, sargs, skwargs = self.strats.pop(0)
                except IndexError:
                    pass  # Nothing there
                else:
                    if not isinstance(signalst, SignalStrategy):
                        # no signal ... reinsert at the beginning
                        self.strats.insert(0, (signalst, sargs, skwargs))
                        signalst = None  # flag as not presetn

            if signalst is None:  # recheck
                # Still None, create a default one
                signalst, sargs, skwargs = SignalStrategy, tuple(), dict()

            # Add the signal strategy
            self.addstrategy(signalst,
                             _accumulate=self._signal_accumulate,
                             _concurrent=self._signal_concurrent,
                             signals=self.signals,
                             *sargs,
                             **skwargs)

        if not self.strats:  # Datas are present, add a strategy
            self.addstrategy(Strategy)

        iterstrats = itertools.product(*self.strats)

        if not self._dooptimize or self.p.maxcpus == 1:
            # If no optimmization is wished ... or 1 core is to be used
            # let's skip process "spawning"
            with tqdm.auto.tqdm(total=self.counter, position=0, leave=True) as pbar:
                for iterstrat in iterstrats:
                    runstrat = self.runstrategies(iterstrat)
                    self.runstrats.append(runstrat)
                    if self._dooptimize:
                        for cb in self.optcbs:
                            cb(runstrat)  # callback receives finished strategy
                    pbar.update(1)
        else:
            if self.p.optdatas and self._dopreload and self._dorunonce:
                for data in self.datas:
                    data.reset()
                    if self._exactbars < 1:  # datas can be full length
                        data.extend(size=self.params.lookahead)
                    data._start()
                    if self._dopreload:
                        data.preload()

            pool = multiprocessing.Pool(self.p.maxcpus or None)
            for r in pool.imap(self, iterstrats):
                self.runstrats.append(r)
                for cb in self.optcbs:
                    cb(r)  # callback receives finished strategy

            pool.close()

            if self.p.optdatas and self._dopreload and self._dorunonce:
                for data in self.datas:
                    data.stop()

        if not self._dooptimize:
            # avoid a list of list for regular cases
            return self.runstrats[0]

        return self.runstrats

    def optstrategy(self, strategy, *args, **kwargs):
        # Default method called
        super().optstrategy(strategy, *args, **kwargs)

        # Then, whe count the number of strats
        self.strats[0], iter = tee(self.strats[0])
        counter = 0
        for strat in iter:
            counter += 1
        self.counter = counter

    def __init__(self):
        super().__init__()
        self.counter = 1
