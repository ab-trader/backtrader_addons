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


class SLTPTracking(bt.Observer):
    '''
    Keep tracking of stop and limit order prices along the backtest. Prices
    should be stored within the strategy in the dictionaries ``sl_price`` and
    ``tp_price`` with the data names used as dictionary keys.    
    '''

    lines = ('stop', 'take')

    plotinfo = dict(plot=True, subplot=False, plotname='SL/TP')

    plotlines = dict(stop=dict(ls=':', linewidth=1.5),
                     take=dict(ls=':', linewidth=1.5),
                     entry=dict(ls='--', linewidth=1.5))


    def next(self):

        if self._owner.sl_price:
            if self._owner.sl_price != 0.0:
                self.lines.stop[0] = self._owner.sl_price

        if self._owner.tp_price:
            if self._owner.tp_price != 0.0:
                self.lines.take[0] = self._owner.tp_price