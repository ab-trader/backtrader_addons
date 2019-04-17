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


class DrawdownPercents(bt.Observer):
    """Reversed drawdown in %s"""

    lines = ('dd', 'maxdd',)

    plotinfo = dict(plot=True, subplot=True, plotname='Drawdown %')

    plotlines = dict(zero=dict(_plotskip=True,),
                     dd=dict(ls='-', linewidth=1.0, color='red'),
                     maxdd=dict(ls='--', linewidth=1.0, color='black',))


    def __init__(self):

        self._dd = self._owner._addanalyzer_slave(bt.analyzers.DrawDown)


    def next(self):

        self.lines.dd[0] = self._dd.rets.drawdown
        self.lines.maxdd[0] = self._dd.rets.max.drawdown
        self.lines.dd[0] = (-1) * self.lines.dd[0]
        self.lines.maxdd[0] = (-1) * self.lines.maxdd[0]


class DrawdownDollars(bt.Observer):
    """Reversed drawdown in $s"""

    lines = ('dd', 'maxdd',)

    plotinfo = dict(plot=True, subplot=True, plotname='Drawdown $')

    plotlines = dict(zero=dict(_plotskip=True,),
                     dd=dict(ls='-', linewidth=1.0, color='red'),
                     maxdd=dict(ls='--', linewidth=1.0, color='black',))


    def __init__(self):

        self._dd = self._owner._addanalyzer_slave(bt.analyzers.DrawDown)


    def next(self):

        self.lines.dd[0] = self._dd.rets.moneydown
        self.lines.maxdd[0] = self._dd.rets.max.moneydown
        self.lines.dd[0] = (-1) * self.lines.dd[0]
        self.lines.maxdd[0] = (-1) * self.lines.maxdd[0]


class DrawdownLength(bt.Observer):
    """Modified drawdown length"""

    lines = ('L', 'maxL',)

    plotinfo = dict(plot=True, subplot=True, plotname='Drawdown Length')

    plotlines = dict(L=dict(ls='-', linewidth=1.0, color='blue'),
                     maxL=dict(ls='--', linewidth=1.0, color='black',))


    def __init__(self):

        self._dd = self._owner._addanalyzer_slave(bt.analyzers.DrawDown)


    def next(self):

        self.lines.L[0] = self._dd.rets.len
        self.lines.maxL[0] = self._dd.rets.max.len