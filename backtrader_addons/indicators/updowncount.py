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


class UpDownNumber(bt.Indicator):
    '''
    Counts number of up (positive value) or down (negative value) candles in
    a row
    '''

    lines = ('count',)

    plotinfo = dict(plot=True, subplot=True)


    def __init__(self):

        c = self.data.close
        o = self.data.open
        self.k = (c > o) - (o > c)
        self.lines.count = bt.LineNum(0)


    def next(self):

        if self.k[0] == self.k[-1]:
            self.lines.count[0] = self.lines.count[-1] + self.k[0]
        else:
            self.lines.count[0] = self.k[0]