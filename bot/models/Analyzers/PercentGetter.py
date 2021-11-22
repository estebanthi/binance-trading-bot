from dataclasses import dataclass
import backtrader as bt
from dataclasses import field


class PercentGetter_analyzer(bt.Analyzer):
    """
    An analyzer to get trades profits percents.
    
    Params :   
        - multiplier : int
            Multiplier of percents. Default is 1. Put it to 100 to get percents in human-readable style
    """

    params = (('multiplier', 1),)

    def __init__(self):

        self.trades = []
        self.side = None

        self.first_loop = False

    def get_analysis(self):
        """
        Return percents

        Returns
        -------

        """
        total_gross, total_net = self.get_percent_sum()
        average_gross, average_net = self.get_average_percent()
        cumulative_gross, cumulative_net = self.get_cumulative_percents()

        return {
            'total_gross': total_gross,
            'average_gross': average_gross,
            'cumulative_gross': cumulative_gross,
            'total_net': total_net,
            'average_net': average_net,
            'cumulative_net': cumulative_net
        }

    def notify_trade(self, trade):
        self.side = 'long' if self.strategy.position.size > 0 else 'short'
        if trade.isclosed:
            percent_gross, percent_net = self.get_percents(trade)
            self.trades.append({
                'percent_gross': percent_gross,
                'percent_net': percent_net
            })



    def get_percent_sum(self):
        """
        Get total sum of percents in trades list.

        Returns
        -------
        sum_gross : float
            Sum percents gross.
        sum_net : float
            Sum percents net.

        """
        sum_gross, sum_net = 0, 0
        for trade in self.trades:
            sum_gross += trade['percent_gross']
            sum_net += trade['percent_net']
        return sum_gross, sum_net

    def get_average_percent(self):
        """
        Get average percents.

        Returns
        -------
        float
            Average gross.
        float
            Average net.

        """
        length = len(self.trades)
        if length > 0:
            return self.get_percent_sum()[0] / length, self.get_percent_sum()[1] / length
        else:
            return 0, 0

    def get_exit_prices(self, trade):
        """
        Get exit prices of a trade.

        Parameters
        ----------
        trade : trade
            Trade.

        Returns
        -------
        exit_price_gross : float
            Exit price.
        exit_price_net : float
            Exit price with fees.

        """
        if self.side == 'long':
            exit_price_net = trade.price + trade.pnlcomm
            exit_price_gross = trade.price + trade.pnl
        if self.side == 'short':
            exit_price_net = trade.price - trade.pnlcomm
            exit_price_gross = trade.price - trade.pnl

        return exit_price_gross, exit_price_net

    def get_percents(self, trade):
        """
        Calculate percents.

        Parameters
        ----------
        trade : trade
            Trade.

        Returns
        -------
        float
            Total gross.
        float
            Total net.

        """
        exit_price_gross, exit_price_net = self.get_exit_prices(trade)

        percent_net = ((exit_price_net / trade.price) - 1) * self.params.multiplier
        percent_gross = ((exit_price_gross / trade.price) - 1) * self.params.multiplier
        if self.side == 'short':
            percent_gross *= -1
            percent_net *= -1

        return percent_gross, percent_net

    def get_cumulative_percents(self):

        cumulative_gross = 1 + self.trades[0]['percent_gross'] / self.params.multiplier
        cumulative_net = 1 + self.trades[0]['percent_net'] / self.params.multiplier

        for trade in self.trades[1:]:
            cumulative_gross *= 1 + trade['percent_gross'] / self.params.multiplier
            cumulative_net *= 1 + trade['percent_net'] / self.params.multiplier

        return (cumulative_gross - 1) * self.params.multiplier, (cumulative_net - 1) * self.params.multiplier


@dataclass
class PercentGetter:
    """
    Get percents on the trade period
    Default name is "percent_getter"

    """
    def __init__(self, multiplier=PercentGetter_analyzer.params.multiplier):
        self.analyzer = PercentGetter_analyzer
        self.parameters = {"multiplier":multiplier, "_name":"percent_getter"}