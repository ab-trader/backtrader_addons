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

import backtrader as bt
import backtrader_addons as bta
import os.path
import sys


class DataTest(bt.Strategy):

    # simple strategy to print the data feed for test needs

    params = (('dt', None),)

    def __init__(self):

        pass
    

    def next(self):
 
        print('%s o: %0.2f, h: %0.2f, l: %0.2f, c: %0.2f, ' % (
            self.data.datetime.date().isoformat(), self.data.open[0],
            self.data.high[0], self.data.low[0], self.data.close[0]) + 
            'v: %0.1f, oi: %0.1f' % (
            self.data.volume[0], self.data.openinterest[0]))


if __name__ == '__main__':

    modpath = os.path.dirname(os.path.abspath(__file__))
    dataspath = '../datas'
    # futures = 'WT.csv'
    futures = 'US2__2019M.csv'
    # futures = 'WT___2019U.csv'

    datapath = os.path.join(modpath, dataspath, futures)

    # --- use case for PremiumDataFut CSV data feed ---
    data = bta.datafeeds.PremiumDataFutCSV(dataname=datapath, plot=True,
                                           name=futures)
    # --- use case for PremiumDataFut CSV data feed ---
    
    cerebro = bt.Cerebro()
    cerebro.addstrategy(DataTest)
    cerebro.adddata(data)
    cerebro.run(stdstats=False)

    cerebro.plot(style='candle', numfigs=1, volup = 'green', voldown = 'red',
                 voltrans = 75.0, voloverlay = False)