# -*- coding: utf-8 -*-

from tabulate import tabulate

class ResultAnalyzer:
    """
    A class to analyze backtesting results.
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
            return sorted({
                tuple(
                    list(
                        dict(result[0].params._getkwargs()).items())) : {
                    'total': result[0].analyzers.trade_analyzer.get_analysis()['pnl']['net']['total'],
                    'average' : result[0].analyzers.trade_analyzer.get_analysis()['pnl']['net']['average']
                    }
                if 'pnl' in result[0].analyzers.trade_analyzer.get_analysis() else
                {
                    'total': 0,
                    'average': 0
                }
                for result in self.result
                }.items(), key = lambda x: x[1]['total'], reverse = True)[:10]
            
    def print_trade_list(self):
        """
        Print trade list.
        Requires tradehistory = True in cerebro.run
        and TradeList analyzer added.

        Returns
        -------
        None.

        """
        
        trade_list = self.result[0].analyzers.trade_list_analyzer.get_analysis()
        print(tabulate(trade_list, headers="keys"))

        to_sum = "chng% pnl% pnl".split()
        sums = [0 for index in range(len(to_sum))]

        for trade in trade_list:
            for index, column in enumerate(to_sum):
                sums[index]+=trade[column]


        for index, name in enumerate(to_sum):
            print(f"Total {name} : {sums[index]}")





        
    