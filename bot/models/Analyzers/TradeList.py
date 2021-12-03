from dataclasses import dataclass
import backtrader as bt
from dataclasses import field


class TradeList_analyzer(bt.Analyzer):
    """
    An analyzer to print data under tabulate format.
    Example : print(tabulate(results[0][0].analyzers.trade_list.get_analysis))
        
     chng%    pnl%    mae%    pricein  ticker      pnl/bar    size     value    mfe%    priceout       pnl    cumpnl  dateout       ref    nbars  dir    datein
-------  ------  ------  ---------  --------  ---------  ------  --------  ------  ----------  --------  --------  ----------  -----  -------  -----  ----------
  -6.07   -2.82  -10.12    281.397  SPY         -271.68     159   44742.1    0.68      264.31  -2716.78  -2716.78  2018-02-14      1       10  long   2018-01-31
  -1.59   -0.71   -2.2     119.128  TLT          -68.55     363   43243.6    1.01      117.24   -685.47  -3402.25  2018-02-22      2       10  long   2018-02-07
   1.21   -0.54   -4.01    268.163  SPY          -51.3     -158  -42369.7    1.44      271.41   -513.04  -3915.29  2018-03-01      3       10  short  2018-02-14
   1.89   -0.84   -2.16    117.946  TLT          -53.82    -363  -42814.4    0.8       120.17   -807.27  -4722.56  2018-03-15      4       15  short  2018-02-22
  -1.98   -1.26   -6       270.915  SPY          -49.35     158   42804.6    3.5       265.55  -1184.35  -5906.91  2018-04-05      5       24  long   2018-03-01
  -1.57    0.71   -0.41    265.55   SPY          336.49    -161  -42753.6    2.84      261.37    672.98  -5233.93  2018-04-09      7        2  short  2018-04-05
   0.93    0.42   -1.09    119.413  TLT           19.87     359   42869.2    2.47      120.52    397.45  -4836.48  2018-04-13      6       20  long   2018-03-15
  -0.89    0.4    -1.35    119.962  TLT           77.43    -361  -43306.4    1.28      118.89    387.13  -4449.35  2018-04-20      9        5  short  2018-04-13
   2.9     1.76   -2.06    264.486  SPY           71.27     165   43126.1    3.28      272.16   1710.47  -2738.88  2018-05-11      8       24  long   2018-04-09
  -0.16    0.07   -0.61    272.585  SPY            6.96    -160  -43613.6    0.94      272.15     69.6   -2669.28  2018-05-25     11       10  short  2018-05-11
   0.95    0.32   -2.43    118.985  TLT           10.37     365   43429.6    2.97      120.11    310.98  -2358.3   2018-06-04     10       30  long   2018-04-20
  -1.18    0.26   -0.32    120.11   TLT           86.15    -182  -21860      1.41      118.69    258.44  -2099.86  2018-06-07     13        3  short  2018-06-04
   0.2     0.09   -0.01    118.69   TLT           29.76     372   44152.7    1.52      118.93     89.28  -2010.58  2018-06-12     14        3  long   2018-06-07
   2.36   -1.08   -3       118.93   TLT          -74.67    -372  -44242      0.25      121.74  -1045.32  -3055.9   2018-07-02     15       14  short  2018-06-12
  -0.78   -0.33   -2.73    275.275  SPY          -11.28     159   43768.8    1.53      273.14   -315.8   -3371.7   2018-07-06     12       28  long   2018-05-25
   1.88   -0.85   -2.3     273.14   SPY         -204.31    -159  -43429.3    0.16      278.28   -817.26  -4188.96  2018-07-12     17        4  short  2018-07-06
  -2.24   -1.01   -2.35    122.013  TLT          -64.31     353   43070.5    0.74      119.28   -964.63  -5153.59  2018-07-24     16       15  long   2018-07-02
   2.55    0.86   -0.24    278.28   SPY           45.82     156   43411.7    2.78      285.39    824.76  -4328.83  2018-08-07     18       18  long   2018-07-12
  -0.02    0.01   -1.01    119.053  TLT            0.81    -362  -43097      0.83      119.03      8.15  -4320.68  2018-08-07     19       10  short  2018-07-24
    
  
    To use : 
        Switch on tradehistory in cerebro. (tradehistory = True)
        Use tabulate :
    from tabulate import tabulate
    trade_list = strats[0].analyzers.trade_list.get_analysis()
    print(tabulate(trade_list, headers="keys"))
        
    
  """

    def get_analysis(self):

        return self.trades

    def __init__(self):

        self.trades = []
        self.cumprofit = 0.0

    def notify_trade(self, trade):

        if trade.isclosed:

            brokervalue = self.strategy.broker.getvalue()

            dir = 'short'
            if trade.history[0].event.size > 0: dir = 'long'

            pricein = trade.history[len(trade.history) - 1].status.price
            priceout = trade.history[len(trade.history) - 1].event.price
            datein = bt.num2date(trade.history[0].status.dt)
            dateout = bt.num2date(trade.history[len(trade.history) - 1].status.dt)
            if trade.data._timeframe >= bt.TimeFrame.Days:
                datein = datein.date()
                dateout = dateout.date()

            pcntchange = 100 * priceout / pricein - 100
            pnl = trade.history[len(trade.history) - 1].status.pnlcomm
            pnlpcnt = 100 * pnl / brokervalue
            barlen = trade.history[len(trade.history) - 1].status.barlen
            pbar = pnl / barlen
            self.cumprofit += pnl

            size = value = 0.0
            for record in trade.history:
                if abs(size) < abs(record.status.size):
                    size = record.status.size
                    value = record.status.value

            highest_in_trade = max(trade.data.high.get(ago=0, size=barlen + 1))
            lowest_in_trade = min(trade.data.low.get(ago=0, size=barlen + 1))
            hp = 100 * (highest_in_trade - pricein) / pricein
            lp = 100 * (lowest_in_trade - pricein) / pricein
            if dir == 'long':
                mfe = hp
                mae = lp
            if dir == 'short':
                mfe = -lp
                mae = -hp

            self.trades.append({'ref': trade.ref, 'ticker': trade.data._name, 'dir': dir,
                                'datein': datein, 'pricein': pricein, 'dateout': dateout, 'priceout': priceout,
                                'chng%': round(pcntchange, 2), 'pnl': pnl, 'pnl%': round(pnlpcnt, 2),
                                'size': size, 'value': value, 'cumpnl': self.cumprofit,
                                'nbars': barlen, 'pnl/bar': round(pbar, 2),
                                'mfe%': round(mfe, 2), 'mae%': round(mae, 2)})


@dataclass
class TradeList:
    """
    Print infos in tradelist format

    """
    analyzer: TradeList_analyzer = TradeList_analyzer
    parameters: dict = field(default_factory=lambda: {'_name': "trade_list"})
