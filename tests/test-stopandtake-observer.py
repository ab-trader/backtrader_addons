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
import sys

import backtrader as bt
import backtrader_addons as bta

from tabulate import tabulate


class SmaCross(bt.SignalStrategy):

    # long-short crossover strategy

    params = (('pfast', 2), ('pslow', 5), ('stop', 150), ('take', 300),
               ('exittype', 'nothing'),)

    def __init__(self):

        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        self.signal = bt.ind.CrossOver(sma1, sma2)

        self.sl_price, self.tp_price = None, None
        self.sl_order, self.tp_order = None, None


    def notify_trade(self, trade):

        if trade.justopened:

            order = self.sell if trade.size > 0 else self.buy

            if 'stop' in self.p.exittype:
                self.sl_price = trade.price - self.p.stop / trade.size
                self.sl_order = order(size=abs(trade.size), price=self.sl_price,
                                      exectype=bt.Order.Stop)
            if 'take' in self.p.exittype:
                self.tp_price = trade.price + self.p.take / trade.size
                self.tp_order = order(size=abs(trade.size), price=self.tp_price,
                                      exectype=bt.Order.Limit)

        if trade.isclosed:

            self.sl_price, self.tp_price = None, None

            if self.sl_order: self.cancel(self.sl_order)
            if self.tp_order: self.cancel(self.tp_order)
            

    def next(self):

        if self.signal > 0:
            self.order_target_size(target=50)
        
        elif self.signal < 0:
            self.order_target_size(target=-50)


if __name__ == '__main__':

    # get script agrument: stoponly, takeonly, stoptake, nothing
    exittype = str(sys.argv[1])

    modpath = os.path.dirname(os.path.abspath(__file__))
    dataspath = '../datas'
    ticker = 'daily_MSFT.csv'
    datapath = os.path.join(modpath, dataspath, ticker)

    cerebro = bt.Cerebro()

    data = bta.datafeeds.AlphavantageCSV(dataname=datapath, datatype='daily')
    cerebro.adddata(data)

    cerebro.addanalyzer(bta.analyzers.trade_list, _name='trade_list')

    # --- add stop-and-take tracking observer to cerebro ---
    cerebro.addobserver(bta.observers.SLTPTracking)
    # --- add stop-and-take tracking observer to cerebro ---

    cerebro.addstrategy(SmaCross, exittype=exittype)
    strats = cerebro.run(tradehistory=True)

    trade_list = strats[0].analyzers.trade_list.get_analysis()
    print (tabulate(trade_list, headers="keys"))

    cerebro.plot(style='candle')