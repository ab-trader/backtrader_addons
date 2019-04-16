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

# import collections
# from datetime import date, time, datetime
# import io
# import itertools
import backtrader as bt

# from backtrader.utils.py3 import (urlopen, urlquote, ProxyHandler, build_opener,
#                                   install_opener)

# from backtrader.utils import date2num

__all__ = ['PremiumDataFutCSV']


class PremiumDataFutCSV(bt.feeds.GenericCSVData):
    '''
    Parses pre-downloaded PremiumData CSV futures data (or locally generated if
    they comply to the PremiumData format) (http://www.premiumdata.net)

    '''

    params = (('dtformat', '%Y%m%d'),)

    # def start(self):

    #     super(PremiumDataFutCSV, self).start()

    #     # Alphavantage data is in reverse order -> reverse
    #     dq = collections.deque()
    #     for line in self.f:
    #         dq.appendleft(line)

    #     f = io.StringIO(newline=None)
    #     f.writelines(dq)
    #     f.seek(0)
    #     self.f.close()
    #     self.f = f


    # def _loadline(self, linetokens):

    #     i = itertools.count(0)

    #     dttxt = linetokens[next(i)]  # YYYY-MM-DD or YYYY-MM-DD HH:MM:SS
    #     dt = date(int(dttxt[0:4]), int(dttxt[5:7]), int(dttxt[8:10]))
    #     tm = self.p.sessionend

    #     # use actual timestamp for INTRADAY time series
    #     if 'INTRADAY' in self.p.datatype:
    #         tm = time(int(dttxt[11:13]), int(dttxt[14:16]), int(dttxt[17:19]))

    #     self.lines.datetime[0] = date2num(datetime.combine(dt, tm))
    #     self.lines.open[0] = float(linetokens[next(i)])
    #     self.lines.high[0] = float(linetokens[next(i)])
    #     self.lines.low[0] = float(linetokens[next(i)])
    #     self.lines.close[0] = float(linetokens[next(i)])

    #     if 'ADJUSTED' in self.p.datatype:
    #         self.lines.adjclose[0] = float(linetokens[next(i)])
    #         self.lines.volume[0] = float(linetokens[next(i)])
    #         self.lines.div[0] = float(linetokens[next(i)])    
    #         # no split data available for WEEKLY or MONTHLY time series        
    #         if ('WEEKLY' in self.p.datatype) or ('MONTHLY' in self.p.datatype):
    #             self.lines.split[0] = 0.0
    #         else:
    #             self.lines.split[0] = float(linetokens[next(i)])
    #     else:
    #         self.lines.volume[0] = float(linetokens[next(i)])
    #         self.lines.adjclose[0] = 0.0
    #         self.lines.div[0] = 0.0
    #         self.lines.split[0] = 0.0

    #     self.lines.openinterest[0] = 0.0

    #     return True