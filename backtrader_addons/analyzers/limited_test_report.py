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
from . import trade_list

class LimitedTestReport(bt.Analyzer):
    '''
    Records results for strategy limited backtest evaluation:

      - ``net_profit``: net profit in $s
      - ``win_percent``: percent of winning trades
      - ``avg_profit``: average profit per trade
      - ``max_dd``: maximum drawdown in $s
      - ``num_trades``: number of trades
      - ``long_trades``: number of long trades
      - ``short_trades``: number of short trades
      - ``max_mfe``: max MFE in $s
      - ``min_mae``: min MAE in $s
      - ``avg_mfe``: average MFE in $s
      - ``avg_mae``: average MAE in $s
    
    Requires backtrader_addons.analyzers.trade_list to be available
    '''

    def get_analysis(self):

        return self.rpt


    def __init__(self):

        self.rpt = dict()
        self._maxdd = bt.analyzers.DrawDown()
        self._trades = trade_list()


    def start(self):

        self.init = self.strategy.broker.getvalue()


    def stop(self):

        drawdowns = self._maxdd.get_analysis()
        trades = self._trades.get_analysis()
        win_percent, avg_trade, long_trades = 0.0, 0.0, 0.0
        avg_mfe, max_mfe = 0.0, 0.0
        avg_mae, min_mae = 0.0, 0.0
        for trade in trades:
            if trade['pnl'] > 0: win_percent += 1
            if trade['dir'] == 'long': long_trades += 1
            avg_trade += trade['pnl']
            avg_mfe += trade['mfe']
            avg_mae += trade['mae']
            max_mfe = max(max_mfe, trade['mfe'])
            min_mae = min(min_mae, trade['mae'])

        self.rpt['net_profit'] = self.strategy.broker.getvalue() - self.init
        self.rpt['max_dd'] = drawdowns.max.moneydown
        self.rpt['num_trades'] = len(trades)
        self.rpt['long_trades'] = long_trades
        self.rpt['short_trades'] = len(trades) - long_trades
        self.rpt['win_percent'] = 100.0 * win_percent / len(trades)
        self.rpt['avg_trade'] = avg_trade / len(trades)
        self.rpt['avg_mfe'] = avg_mfe / len(trades)
        self.rpt['avg_mae'] = avg_mae / len(trades)
        self.rpt['max_mfe'] = max_mfe
        self.rpt['min_mae'] = min_mae