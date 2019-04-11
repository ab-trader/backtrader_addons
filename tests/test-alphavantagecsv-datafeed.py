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


if __name__ == '__main__':

    cerebro = bt.Cerebro()

    modpath = os.path.dirname(os.path.abspath(__file__))
    dataspath = '../datas'
    tickers = ['SPY-alphavantage.csv', 'TQQQ-alphavantage.csv']

    for i in tickers:
        datapath = os.path.join(modpath, dataspath, i)
        data = bta.datafeeds.AlphavantageCSVData(
            dataname=datapath,
            plot=True,
            plotylimited=False,
            name=i)
        cerebro.adddata(data)

    strats = cerebro.run(stdstats=False)

    cerebro.plot(style='line', numfigs=1, volup = 'green', voldown = 'red',
                 voltrans = 75.0, voloverlay = False)