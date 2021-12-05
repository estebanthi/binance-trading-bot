# -*- coding: utf-8 -*-

from tabulate import tabulate
from termcolor import colored

class ResultsAnalyzer:
    """
    A class to analyze backtesting results.

    Warning : it's not an usual analyzer, you can't add it to Engine
    You have to instantiate it after results have been created

    """
    
    def __init__(self, result):
        """
        Constructor.

        Parameters
        ----------
        result : bt.result
            Result of the backtest.

        Returns
        -------
        None.

        """
        self.result = result
    
    
    def get_pnls(self):
        """
        Get PNLS.
        Requires TradeAnalyzer added.

        Returns
        -------
        dict
            Dict of pnls.

        """
        
        if type(self.result[0]) is not list:
            return dict(self.result[0].analyzers.trade_analyzer.get_analysis()['pnl']['net'])
        
        else:
            pnls_dict = {}
            for result in self.result:  # For loop for iterating in all strats
                for strat in result:
                    analysis = strat.analyzers.trade_analyzer.get_analysis()
                    pnl_dict = {    # Default dict if no PNL
                        "total": 0,
                        "average": 0,
                    }
                    if "pnl" in analysis:
                        pnl_dict = {
                            "total": strat.analyzers.trade_analyzer.get_analysis()['pnl']['net']['total'],
                            "average": strat.analyzers.trade_analyzer.get_analysis()['pnl']['net']['average'],
                        }

                    key = tuple(    # Dict's key is a tuple containing strat parameters
                            list(
                                dict(strat.params._getkwargs()).items()))

                    pnls_dict[key] = pnl_dict

            return sorted(pnls_dict.items(), key = lambda x: x[1]['total'], reverse = True)[:10]



            
    def print_trade_list(self):
        """
        Print trade list
        Requires tradehistory and TradeList analyzer in Engine

        Returns
        -------
        None.

        """

        trade_list = self.result[0][0].analyzers.trade_list.get_analysis()
        print(tabulate(trade_list, headers="keys"))

        to_sum = "chng% pnl% pnl".split()
        sums = [0 for index in range(len(to_sum))]

        for trade in trade_list:
            for index, column in enumerate(to_sum):
                sums[index]+=trade[column]


        for index, name in enumerate(to_sum):
            print(f"Total {name} : {sums[index]}")


    def pretty_pnls(self):
        """
        Render pnls in a prettier format
        """

        pnls = self.get_pnls()

        del_params = "logging recurring_recap".split(" ")

        params_dict = []
        for pnl_dict in pnls:
            pnl_subdict = dict(pnl_dict[0])
            for param in del_params:
                if param in pnl_subdict:
                    del pnl_subdict[param]
            params_dict.append(pnl_subdict)


        for index, subdict in enumerate(params_dict):
            print("\n")
            print(f"Strat {index+1} : ")
            for param, value in subdict.items():
                print(param, value)
            print(f"\nTotal PNL : {pnls[index][1]['total']}")
            print(f"Average PNL : {pnls[index][1]['average']}")


    def print_metrics(self):

        metrics = self.result[0][0].analyzers.full_metrics.get_analysis()
        metrics_list = []
        for k, v in metrics.items():

            if isinstance(v, float):
                v = round(v, 2)

            if k in "Annual returns, Average drawdown, Max drawdown, Returns volatility, Average return per trade, Average return per long, " \
                    "Average return per short, Winrate".split(", "):
                v = f"{v} %"

            color = "white"
            if k in "Annual returns, PNL net, Fees, Winrate".split(", "):
                color = "green"
            if k in "Average return per trade, Total trades, Total long, Total short, Open trades, Average return per long, Average return per short".split(", "):
                color = "blue"
            if k in "Time in market, Average trade len, Max trade len, Average won len, Average lost len".split(", "):
                color = "magenta"
            if k in "Average drawdown, Average drawdown length, Max drawdown, Max drawdown length".split(", "):
                color = "red"
            if k in "Annualized Sharpe ratio, Returns volatility, Calmar ratio".split(", "):
                color = "yellow"
            k, v = colored(k, color, attrs=["bold"]), colored(v, color)



            metrics_list.append([k, v])

        print(tabulate(metrics_list, tablefmt="grid"))


        
    