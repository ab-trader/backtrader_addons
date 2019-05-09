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

class trade_list(bt.Analyzer):
    '''
    Records closed trades and returns dictionary containing the following
    keys/values:

      - ``ref``: reference number (from backtrader)
      - ``ticker``: data name
      - ``dir``: direction (long or short)
      - ``datein``: entry date/time
      - ``pricein``: entry price (considering multiple entries)
      - ``dateout``: exit date/time
      - ``priceout``: exit price (considering multiple exits)
      - ``chng%``: price change in %s during trade
      - ``pnl``: profit/loss
      - ``pnl%``: profit/loss in % to broker value
      - ``size``: size
      - ``value``: value
      - ``cumpnl``: cumulative profit/loss for trades shown before this trade
      - ``nbars``: average trade duration in price bars
      - ``pnl/bar``: average profit/loss per bar
      - ``mfe``: max favorable excursion in $s from entry price
      - ``mae``: max adverse excursion in $s from entry price
      - ``mfe%``: max favorable excursion in % of entry price
      - ``mae%``: max adverse excursion in % of entry price
    '''

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

            pricein = trade.history[len(trade.history)-1].status.price
            priceout = trade.history[len(trade.history)-1].event.price
            datein = bt.num2date(trade.history[0].status.dt)
            dateout = bt.num2date(trade.history[len(trade.history)-1].status.dt)
            if trade.data._timeframe >= bt.TimeFrame.Days:
                datein = datein.date()
                dateout = dateout.date()

            pcntchange = 100 * priceout / pricein - 100
            pnl = trade.history[len(trade.history)-1].status.pnlcomm
            pnlpcnt = 100 * pnl / brokervalue
            barlen = trade.history[len(trade.history)-1].status.barlen
            pbar = pnl / barlen
            self.cumprofit += pnl

            size = value = 0.0
            for record in trade.history:
                if abs(size) < abs(record.status.size):
                    size = record.status.size
                    value = record.status.value

            highest_in_trade = max(trade.data.high.get(ago=0, size=barlen+1))
            lowest_in_trade = min(trade.data.low.get(ago=0, size=barlen+1))
            hp = highest_in_trade - pricein
            lp = lowest_in_trade - pricein
            if dir == 'long':
                mfe0 = hp
                mae0 = lp
                mfe = 100 * hp / pricein
                mae = 100 * lp / pricein
            if dir == 'short':
                mfe0 = -lp
                mae0 = -hp
                mfe = -100 * lp / pricein
                mae = -100 * hp / pricein

            self.trades.append({'ref': trade.ref, 'ticker': trade.data._name,
                'dir': dir, 'datein': datein, 'pricein': pricein,
                'dateout': dateout, 'priceout': priceout,
                 'chng%': round(pcntchange, 2), 'pnl': pnl,
                 'pnl%': round(pnlpcnt, 2), 'size': size, 'value': value,
                 'cumpnl': self.cumprofit, 'nbars': barlen,
                 'pnl/bar': round(pbar, 2), 'mfe': round(mfe0, 2),
                 'mae': round(mae0, 2), 'mfe%': round(mfe, 2),
                 'mae%': round(mae, 2)})