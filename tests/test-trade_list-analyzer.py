# Copyright (C) 2019  ab-trader

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os.path
from tabulate import tabulate

import backtrader as bt
import backtrader_addons as bta

class SmaCross(bt.SignalStrategy):

    # long-short crossover strategy

    params = (('pfast', 2), ('pslow', 5),)

    def __init__(self):

        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        self.signal = bt.ind.CrossOver(sma1, sma2)


    def next(self):

        if self.signal > 0:
            self.order_target_size(target=-50)
        
        elif self.signal < 0:
            self.order_target_size(target=50)


if __name__ == '__main__':

    modpath = os.path.dirname(os.path.abspath(__file__))
    dataspath = '../datas'
    ticker = 'daily_MSFT.csv'
    datapath = os.path.join(modpath, dataspath, ticker)

    cerebro = bt.Cerebro()

    data = bta.datafeeds.AlphavantageCSV(dataname=datapath, datatype='daily')
    cerebro.adddata(data)

    # --- add trade_list analyzer to cerebro ---
    cerebro.addanalyzer(bta.analyzers.trade_list, _name='trade_list')
    # --- add trade_list analyzer to cerebro ---

    cerebro.addstrategy(SmaCross)
    # --- turn on tradehistory writing in cerebro ---
    strats = cerebro.run(tradehistory=True)
    # --- turn on tradehistory writing in cerebro ---

    # --- get trade_list results and print them in nice format ---
    trade_list = strats[0].analyzers.trade_list.get_analysis()
    print (tabulate(trade_list, headers="keys"))
    # --- get trade_list results and print them in nice format ---

    cerebro.plot()