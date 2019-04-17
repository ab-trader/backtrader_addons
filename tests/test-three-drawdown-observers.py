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
            self.order_target_size(target=50)
        
        elif self.signal < 0:
            self.order_target_size(target=-50)


if __name__ == '__main__':

    modpath = os.path.dirname(os.path.abspath(__file__))
    dataspath = '../datas'
    ticker = 'daily_MSFT.csv'
    datapath = os.path.join(modpath, dataspath, ticker)

    cerebro = bt.Cerebro()

    data = bta.datafeeds.AlphavantageCSV(dataname=datapath, datatype='daily')
    cerebro.adddata(data)

    # --- add three drawdown observers to cerebro ---
    cerebro.addobserver(bta.observers.DrawdownPercents)
    cerebro.addobserver(bta.observers.DrawdownDollars)
    cerebro.addobserver(bta.observers.DrawdownLength)
    # --- add three drawdown observers to cerebro ---

    cerebro.addstrategy(SmaCross)
    strats = cerebro.run()

    cerebro.plot()