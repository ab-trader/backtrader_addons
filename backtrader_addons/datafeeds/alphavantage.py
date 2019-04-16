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

import collections
from datetime import date, time, datetime
import io
import itertools
import backtrader as bt

from backtrader.utils.py3 import (urlopen, urlquote, ProxyHandler, build_opener,
                                  install_opener)

from backtrader.utils import date2num

__all__ = ['AlphavantageCSV', 'Alphavantage']


class AlphavantageCSV(bt.CSVDataBase):
    '''
    Parses pre-downloaded Alphavantage CSV Stock Time Series Data (or locally
    generated if they comply to the Alphavantage format)
    (https://www.alphavantage.co/documentation/#time-series-data)

    Specific parameters:
      - ``dataname``: The filename to parse or a file-like object
      - ``datatype``: (default: ``DAILY``) Type of the time series
                      (see Alphavantage API, function parameter).
    '''

    _online = False

    params = (('datatype', 'DAILY_ADJUSTED'),)

    lines = ('adjclose', 'div', 'split')


    def start(self):

        super(AlphavantageCSV, self).start()

        if self._online:
            self.p.datatype = self.p.function

        # Alphavantage data is in reverse order -> reverse
        dq = collections.deque()
        for line in self.f:
            dq.appendleft(line)

        f = io.StringIO(newline=None)
        f.writelines(dq)
        f.seek(0)
        self.f.close()
        self.f = f


    def _loadline(self, linetokens):

        i = itertools.count(0)

        dttxt = linetokens[next(i)]  # YYYY-MM-DD or YYYY-MM-DD HH:MM:SS
        dt = date(int(dttxt[0:4]), int(dttxt[5:7]), int(dttxt[8:10]))
        tm = self.p.sessionend

        # use actual timestamp for INTRADAY time series
        if 'INTRADAY' in self.p.datatype:
            tm = time(int(dttxt[11:13]), int(dttxt[14:16]), int(dttxt[17:19]))

        self.lines.datetime[0] = date2num(datetime.combine(dt, tm))
        self.lines.open[0] = float(linetokens[next(i)])
        self.lines.high[0] = float(linetokens[next(i)])
        self.lines.low[0] = float(linetokens[next(i)])
        self.lines.close[0] = float(linetokens[next(i)])

        if 'ADJUSTED' in self.p.datatype:
            self.lines.adjclose[0] = float(linetokens[next(i)])
            self.lines.volume[0] = float(linetokens[next(i)])
            self.lines.div[0] = float(linetokens[next(i)])    
            # no split data available for WEEKLY or MONTHLY time series        
            if ('WEEKLY' in self.p.datatype) or ('MONTHLY' in self.p.datatype):
                self.lines.split[0] = 0.0
            else:
                self.lines.split[0] = float(linetokens[next(i)])
        else:
            self.lines.volume[0] = float(linetokens[next(i)])
            self.lines.adjclose[0] = 0.0
            self.lines.div[0] = 0.0
            self.lines.split[0] = 0.0

        self.lines.openinterest[0] = 0.0

        return True


class Alphavantage(AlphavantageCSV):
    '''
    Executes a direct download of Stock Time Series data from Alphavantage
    servers (https://www.alphavantage.co/documentation/#time-series-data)

    Specific parameters (or specific meaning):
      - ``dataname``: The ticker to download ('YHOO' for example)
      - ``baseurl``:  The server url. Someone might decide to open a
                      Alphavantage compatible service in the future.
      - ``function``: (default: ``DAILY_ADJUSTED``) (see Alphavantage API)
      - ``interval``: (default: 15) (see Alphavantage API)
      - ``outputsize``: (default: ``full``) (see Alphavantage API)
      - ``apikey``: API key (see Alphavantage API)
      - ``buffered``: (default: True) If True the entire socket connection wil
                      be buffered locally before parsing starts.
      '''
    
    _online = True

    params = (
        ('baseurl', 'https://www.alphavantage.co/query?'),
        ('function', 'DAILY_ADJUSTED'),
        ('interval', 15),
        ('outputsize', 'full'),
        ('apikey', 'demo'),
        ('buffered', True),
    )


    def start(self):

        self.error = None

        url = '{}function=TIME_SERIES_{}&symbol={}'.format(
            self.p.baseurl, self.p.function, urlquote(self.p.dataname))

        urlargs = []
        if self.p.function == 'INTRADAY':
            urlargs.append('interval=%dmin' % self.p.interval)

        if self.p.apikey is not None:
            urlargs.append('apikey={}'.format(self.p.apikey))

        urlargs.append('datatype=csv')

        if urlargs:
            url += '&' + '&'.join(urlargs)

        try:
            datafile = urlopen(url)
        except IOError as e:
            self.error = str(e)
            # leave us empty
            return

        if self.p.buffered:
            # buffer everything from the socket into a local buffer
            f = io.StringIO(datafile.read().decode('utf-8'), newline=None)
            datafile.close()
        else:
            f = datafile

        self.f = f

        # Prepared a "path" file -  CSV Parser can take over
        super(Alphavantage, self).start()