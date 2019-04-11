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
import datetime
import itertools


class AlphavantageCSVData(bt.CSVDataBase):
    """
    CSV data feed for Alphavantage adjusted daily time series
    """

    lines = ('adjclose', 'div', 'split')

    params = (('adjclose', 5), ('volume', 6), ('div', 7), ('split', 8),)


    def start(self):

        super(AlphavantageCSVData, self).start()


    def stop(self):

        pass


    def _loadline(self, linetokens):

        i = itertools.count(0)

        dttxt = linetokens[next(i)]
        y = int(dttxt[0:4])
        m = int(dttxt[5:7])
        d = int(dttxt[8:10])

        dt = datetime.datetime(y, m, d)
        dtnum = bt.date2num(dt)

        self.lines.datetime[0] = dtnum
        self.lines.open[0] = float(linetokens[next(i)])
        self.lines.high[0] = float(linetokens[next(i)])
        self.lines.low[0] = float(linetokens[next(i)])
        self.lines.close[0] = float(linetokens[next(i)])
        self.lines.adjclose[0] = float(linetokens[next(i)])
        self.lines.volume[0] = float(linetokens[next(i)])
        self.lines.div[0] = float(linetokens[next(i)])
        self.lines.split[0] = float(linetokens[next(i)])

        return True