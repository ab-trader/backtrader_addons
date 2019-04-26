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

# TODO setup hover tool
# TODO plot volume chart

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import collections, math
import pdb

from bokeh.models.widgets import Panel, Tabs
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool

import backtrader as bt
from backtrader.utils.py3 import with_metaclass
from .scheme import PlotScheme

class PInfo(object):

    # TODO This class is default backtrader plotting class.
    
    def __init__(self, sch):
        self.sch = sch
        self.nrows = 0
        self.row = 0
        self.clock = None
        self.x = None
        self.xlen = 0
        self.sharex = None
        self.figs = list()
        self.cursors = list()
        self.daxis = collections.OrderedDict()
        self.vaxis = list()
        self.coloridx = collections.defaultdict(lambda: -1)
        self.handles = collections.defaultdict(list)
        self.labels = collections.defaultdict(list)
        self.legpos = collections.defaultdict(int)


    def newfig(self, figid, numfig, mpyplot):
        fig = mpyplot.figure(figid + numfig)
        self.figs.append(fig)
        self.daxis = collections.OrderedDict()
        self.vaxis = list()
        self.row = 0
        self.sharex = None
        return fig

    def nextcolor(self, ax): # * IN USE
        self.coloridx[ax] += 1
        return self.coloridx[ax]

    def color(self, ax): # * IN USE
        return self.sch.color(self.coloridx[ax])


class BokehPlotter(with_metaclass(bt.MetaParams, object)):

    params = (('scheme', PlotScheme()),)

    def __init__(self, **kwargs):
        for pname, pvalue in kwargs.items():
            setattr(self.p.scheme, pname, pvalue)


    def plot(self, strategy, figid=0, numfigs=1, iplot=False,
             start=None, end=None, use=None):
        '''
        Creates html file with bokeh plot for single "strategy"
        
        "figid": strategy id
        "numfigs": left for compatibility with cerebro.plot()
        "iplot": doesn't support jupyter notebook
        "start": an index to the datetime line array of the strategy or a
                 datetime.date, datetime.datetime instance indicating the
                 start of the plot
        "end": an index to the datetime line array of the strategy or a
               datetime.date, datetime.datetime instance indicating the end of
               the plot
        "use": left for compatibility with cerebro.plot()
        '''

        if not strategy.datas:
            return

        if not len(strategy):
            return

        # if iplot:
        #     if 'ipykernel' in sys.modules:
        #         matplotlib.use('nbagg')

        # # this import must not happen before matplotlib.use
        # import matplotlib.pyplot as mpyplot
        # self.mpyplot = mpyplot

        self.pinf = PInfo(self.p.scheme)
        # sort all information to be plotted
        self.sortdataindicators(strategy)
        # self.calcrows(strategy)

        pdb.set_trace()

        self.dt_axis=[bt.num2date(x) for x in strategy.datetime.array.tolist()]

        # st_dtime = strategy.lines.datetime.plot()
        # if start is None:
        #     start = 0
        # if end is None:
        #     end = len(st_dtime)

        # if isinstance(start, datetime.date):
        #     start = bisect.bisect_left(st_dtime, date2num(start))

        # if isinstance(end, datetime.date):
        #     end = bisect.bisect_right(st_dtime, date2num(end))

        # if end < 0:
        #     end = len(st_dtime) + 1 + end  # -1 =  len() -2 = len() - 1

        # slen = len(st_dtime[start:end])
        # d, m = divmod(slen, numfigs)
        # pranges = list()
        # for i in range(numfigs):
        #     a = d * i + start
        #     if i == (numfigs - 1):
        #         d += m  # add remainder to last stint
        #     b = a + d

        #     pranges.append([a, b, d])

        # figs = []

        # for numfig in range(numfigs):
        #     # prepare a figure
        #     fig = self.pinf.newfig(figid, numfig, self.mpyplot)
        #     figs.append(fig)

        #     self.pinf.pstart, self.pinf.pend, self.pinf.psize = pranges[numfig]
        #     self.pinf.xstart = self.pinf.pstart
        #     self.pinf.xend = self.pinf.pend

        #     self.pinf.clock = strategy
        #     self.pinf.xreal = self.pinf.clock.datetime.plot(
        #         self.pinf.pstart, self.pinf.psize)
        #     self.pinf.xlen = len(self.pinf.xreal)
        #     self.pinf.x = list(range(self.pinf.xlen))
        #     # self.pinf.pfillers = {None: []}
        #     # for key, val in pfillers.items():
        #     #     pfstart = bisect.bisect_left(val, self.pinf.pstart)
        #     #     pfend = bisect.bisect_right(val, self.pinf.pend)
        #     #     self.pinf.pfillers[key] = val[pfstart:pfend]

        # setup output file
        output_file('strategy_%d.html' % figid, title='strategy #%d' % figid)
        
        self.figs = []
        obs_tab = []

        # Do the plotting
        #     # Things that go always at the top (observers)
        #     self.pinf.xdata = self.pinf.x

        # plot graphs on the top (observers)
        for ptop in self.dplotstop:
            self.plotind(None, ptop, subinds=self.dplotsover[ptop])
        
        if not self.pinf.sch.btlayout:
            obs_tab.append(Panel(child=column(self.figs), title='OBSERVERS'))
            self.figs = []

        #     # Create the rest on a per data basis
        #     dt0, dt1 = self.pinf.xreal[0], self.pinf.xreal[-1]
        #     for data in strategy.datas:
        #         if not data.plotinfo.plot:
        #             continue

        #         self.pinf.xdata = self.pinf.x
        #         xd = data.datetime.plotrange(self.pinf.xstart, self.pinf.xend)
        #         if len(xd) < self.pinf.xlen:
        #             self.pinf.xdata = xdata = []
        #             xreal = self.pinf.xreal
        #             dts = data.datetime.plot()
        #             xtemp = list()
        #             for dt in (x for x in dts if dt0 <= x <= dt1):
        #                 dtidx = bisect.bisect_left(xreal, dt)
        #                 xdata.append(dtidx)
        #                 xtemp.append(dt)

        #             self.pinf.xstart = bisect.bisect_left(dts, xtemp[0])
        #             self.pinf.xend = bisect.bisect_right(dts, xtemp[-1])

        data_tabs = []
        # plot other graphs on datas
        for data in strategy.datas:
            if data.plotinfo.plot:

                for ind in self.dplotsup[data]:
                    self.plotind(data, ind,
                        subinds=self.dplotsover[ind],
                        upinds=self.dplotsup[ind],
                        downinds=self.dplotsdown[ind])

                self.plotdata(data, self.dplotsover[data])

                for ind in self.dplotsdown[data]:
                    self.plotind(data, ind,
                        subinds=self.dplotsover[ind],
                        upinds=self.dplotsup[ind],
                        downinds=self.dplotsdown[ind])

                if not self.pinf.sch.btlayout:
                    data_tabs.append(
                        Panel(child=column(self.figs), title=data._name))
                    self.figs= []

        #     cursor = MultiCursor(
        #         fig.canvas, list(self.pinf.daxis.values()),
        #         useblit=True,
        #         horizOn=True, vertOn=True,
        #         horizMulti=False, vertMulti=True,
        #         horizShared=True, vertShared=False,
        #         color='black', lw=1, ls=':')

        #     self.pinf.cursors.append(cursor)

        #     # Put the subplots as indicated by hspace
        #     fig.subplots_adjust(hspace=self.pinf.sch.plotdist,
        #                         top=0.98, left=0.05, bottom=0.05, right=0.95)

        #     laxis = list(self.pinf.daxis.values())

        #     # Find last axis which is not a twinx (date locator fails there)
        #     i = -1
        #     while True:
        #         lastax = laxis[i]
        #         if lastax not in self.pinf.vaxis:
        #             break

        #         i -= 1

        #     self.setlocators(lastax)  # place the locators/fmts

        #     # Applying fig.autofmt_xdate if the data axis is the last one
        #     # breaks the presentation of the date labels. why?
        #     # Applying the manual rotation with setp cures the problem
        #     # but the labels from all axis but the last have to be hidden
        #     for ax in laxis:
        #         self.mpyplot.setp(ax.get_xticklabels(), visible=False)

        #     self.mpyplot.setp(lastax.get_xticklabels(), visible=True,
        #                       rotation=self.pinf.sch.tickrotation)

        #     # Things must be tight along the x axis (to fill both ends)
        #     axtight = 'x' if not self.pinf.sch.ytight else 'both'
        #     self.mpyplot.autoscale(enable=True, axis=axtight, tight=True)

        if self.pinf.sch.btlayout and not len(self.figs):
             return

        if (not self.pinf.sch.btlayout and
                                    not len(obs_tab) and not len(data_tabs)):
             return

        # show plots
        if self.pinf.sch.btlayout:
            print('LOG: total number of figures is %d' % len(self.figs))
            show(column(self.figs))
        else:
            print('LOG: multiple tabs layout of %d tabs'
                                                    % len(obs_tab+data_tabs))
            show(Tabs(tabs=obs_tab+data_tabs))

        return self.figs


    def show(self):
        '''
        Left to maintain compatibilty with cerebro.plot()
        '''

        return

    
    def sortdataindicators(self, strategy):
        '''
        Sort data feeds, indicators and observers
        (copy from original plotting script)
        '''

        # These lists/dictionaries hold the subplots that go above each data
        self.dplotstop = list()
        self.dplotsup = collections.defaultdict(list)
        self.dplotsdown = collections.defaultdict(list)
        self.dplotsover = collections.defaultdict(list)

        # Sort observers in the different lists/dictionaries
        for x in strategy.getobservers():
            if not x.plotinfo.plot or x.plotinfo.plotskip:
                continue

            if x.plotinfo.subplot:
                self.dplotstop.append(x)
            else:
                key = getattr(x._clock, 'owner', x._clock)
                self.dplotsover[key].append(x)

        # Sort indicators in the different lists/dictionaries
        for x in strategy.getindicators():
            if not hasattr(x, 'plotinfo'):
                # no plotting support - so far LineSingle derived classes
                continue

            if not x.plotinfo.plot or x.plotinfo.plotskip:
                continue

            x._plotinit()  # will be plotted ... call its init function

            # support LineSeriesStub which has "owner" to point to the data
            key = getattr(x._clock, 'owner', x._clock)
            if key is strategy:  # a LinesCoupler
                key = strategy.data

            if getattr(x.plotinfo, 'plotforce', False):
                if key not in strategy.datas:
                    while True:
                        if key not in strategy.datas:
                            key = key._clock
                        else:
                            break

            xpmaster = x.plotinfo.plotmaster
            if xpmaster is x:
                xpmaster = None
            if xpmaster is not None:
                key = xpmaster

            if x.plotinfo.subplot and xpmaster is None:
                if x.plotinfo.plotabove:
                    self.dplotsup[key].append(x)
                else:
                    self.dplotsdown[key].append(x)
            else:
                self.dplotsover[key].append(x)

    
    def plotind(self, iref, ind, 
                subinds=None, upinds=None, downinds=None, masterax=None):
        '''
        Creates single bokeh figure for observer or indicator
        '''

        # sch = self.p.scheme

        # check subind
        subinds = subinds or []
        upinds = upinds or []
        downinds = downinds or []

        # plot subindicators on self with independent axis above
        for upind in upinds:
            self.plotind(iref, upind)
    
        indlabel = ind.plotlabel()

        # Get a figure for this plot
        fig = masterax or self.new_figure(pwidth=self.pinf.sch.fwidth,
                                          pheight=self.pinf.sch.fiheight,
                                          ptitle=indlabel)

        print('LOG: plotind - ind - %s' % (ind.plotlabel()))

        for lineidx in range(ind.size()):
            line = ind.lines[lineidx]
            linealias = ind.lines._getlinealias(lineidx)

            lineplotinfo = getattr(ind.plotlines, '_%d' % lineidx, None)
            if not lineplotinfo:
                lineplotinfo = getattr(ind.plotlines, linealias, None)

            if not lineplotinfo:
                lineplotinfo = bt.AutoInfoClass()

            if lineplotinfo._get('_plotskip', False):
                continue

            # Legend label only when plotting 1st line
            if masterax and not ind.plotinfo.plotlinelabels:
                label = indlabel * (lineidx == 0) or None
            else:
                label = ''
                label += lineplotinfo._get('_name', '') or linealias

            # plot data
            lplot = line.array.tolist()
        #     lplot = line.plotrange(self.pinf.xstart, self.pinf.xend)

            # Global and generic for indicator
            if self.pinf.sch.linevalues and ind.plotinfo.plotlinevalues:
                plotlinevalue = lineplotinfo._get('_plotvalue', True)
                if plotlinevalue and not math.isnan(lplot[-1]) and label:
                    label += ' %.2f' % lplot[-1]

            plotkwargs = dict()
            linekwargs = lineplotinfo._getkwargs(skip_=True)

            # matplotlib to bokeh translation:
            # color translation
            if linekwargs.get('color', None):
                if not lineplotinfo._get('_samecolor', False):
                    color_mpl = linekwargs.get('color', None)
                    color = self.pinf.sch.translate_color(color_mpl)
                    plotkwargs['fill_color'] = color
                    plotkwargs['line_color'] = color
            else:
                if linekwargs.get('line_color', None) is None:
                    if not lineplotinfo._get('_samecolor', False):
                        self.pinf.nextcolor(fig)
                    plotkwargs['line_color'] = self.pinf.color(fig)

            # line type translation
            mpl_ls = ['-', '--', '-.', ':', 'solid', 'dashed',
                      'dashdot', 'dotted', None, ' ', '']
            bokeh_ls = ['solid', 'dashed', 'dashdot', 'dotdash', 'solid',
                        'dashed', 'dashdot', 'dotdash', None, ' ', '']
            if linekwargs.get('ls', None) or linekwargs.get('linestyle', None):
                ls_mpl = linekwargs.get('ls', None)
                ls_bokeh = bokeh_ls[mpl_ls.index(ls_mpl)]
                plotkwargs['line_dash'] = ls_bokeh
            else:
                if linekwargs.get('line_dash', None) is None:
                    plotkwargs['line_dash'] = 'solid'

            # marker type translation
            if linekwargs.get('marker', None):
                marker_mpl = linekwargs.get('marker', None)
                m, f = self.pinf.sch.translate_marker(marker_mpl)
                plotkwargs['marker'] = m
                if f:
                    plotkwargs['fill_color'] = plotkwargs['line_color']
                else:
                    plotkwargs['fill_color'] = None

            plotkwargs.update(dict(legend=label))
            # plotkwargs.update(**linekwargs)

            # define figure type for the line
            # pltmethod = getattr(fig, lineplotinfo._get('_method', 'line'))
            pltmethod = lineplotinfo._get('_method', 'line')
                
            xdata, lplotarray = self.dt_axis, lplot
        #     xdata, lplotarray = self.pinf.xdata, lplot
        #     if lineplotinfo._get('_skipnan', False):
        #         # Get the full array and a mask to skipnan
        #         lplotarray = np.array(lplot)
        #         lplotmask = np.isfinite(lplotarray)

        #         # Get both the axis and the data masked
        #         lplotarray = lplotarray[lplotmask]
        #         xdata = np.array(xdata)[lplotmask]

            # * temporary use before full plotkwargs implementation
            if pltmethod == 'line':
                if linekwargs.get('marker', None):
                    fig.scatter(xdata, lplotarray, legend=label,
                                marker=plotkwargs['marker'],
                                fill_color=plotkwargs['fill_color'],
                                line_color=plotkwargs['line_color'],
                                size=10.0)
                else:
                    fig.line(xdata, lplotarray, legend=label,
                             line_width=self.pinf.sch.lwidth,
                             line_color=plotkwargs['line_color'],
                             line_dash=plotkwargs['line_dash'])

        #     vtags = lineplotinfo._get('plotvaluetags', True)
        #     if self.pinf.sch.valuetags and vtags:
        #         linetag = lineplotinfo._get('_plotvaluetag', True)
        #         if linetag and not math.isnan(lplot[-1]):
        #             # line has valid values, plot a tag for the last value
        #             self.drawtag(ax, len(self.pinf.xreal), lplot[-1],
        #                          facecolor='white',
        #                          edgecolor=self.pinf.color(ax))

        #     farts = (('_gt', operator.gt), ('_lt', operator.lt), ('', None),)
        #     for fcmp, fop in farts:
        #         fattr = '_fill' + fcmp
        #         fref, fcol = lineplotinfo._get(fattr, (None, None))
        #         if fref is not None:
        #             y1 = np.array(lplot)
        #             if isinstance(fref, integer_types):
        #                 y2 = np.full_like(y1, fref)
        #             else:  # string, naming a line, nothing else is supported
        #                 l2 = getattr(ind, fref)
        #                 prl2 = l2.plotrange(self.pinf.xstart, self.pinf.xend)
        #                 y2 = np.array(prl2)
        #             kwargs = dict()
        #             if fop is not None:
        #                 kwargs['where'] = fop(y1, y2)

        #             falpha = self.pinf.sch.fillalpha
        #             if isinstance(fcol, (list, tuple)):
        #                 fcol, falpha = fcol

        #             ax.fill_between(self.pinf.xdata, y1, y2,
        #                             facecolor=fcol,
        #                             alpha=falpha,
        #                             interpolate=True,
        #                             **kwargs)
            print('LOG: plotind - line - %s' % label)

        # plot subindicators that were created on self
        for subind in subinds:
            self.plotind(iref, subind, subinds=self.dplotsover[subind],
                         masterax=fig)
        
        if not masterax:
            fig.legend.location=self.pinf.sch.legendindloc
            fig.legend.label_text_font_size = '8pt'
            self.figs.append(fig)

        #     # adjust margin if requested ... general of particular
        #     ymargin = ind.plotinfo._get('plotymargin', 0.0)
        #     ymargin = max(ymargin, self.pinf.sch.yadjust)
        #     if ymargin:
        #         ax.margins(y=ymargin)

        #     # Set specific or generic ticks
        #     yticks = ind.plotinfo._get('plotyticks', [])
        #     if not yticks:
        #         yticks = ind.plotinfo._get('plotyhlines', [])

        #     if yticks:
        #         ax.set_yticks(yticks)
        #     else:
        #         locator = mticker.MaxNLocator(nbins=4, prune='both')
        #         ax.yaxis.set_major_locator(locator)

        #     # Set specific hlines if asked to
        #     hlines = ind.plotinfo._get('plothlines', [])
        #     if not hlines:
        #         hlines = ind.plotinfo._get('plotyhlines', [])
        #     for hline in hlines:
        #         ax.axhline(hline, color=self.pinf.sch.hlinescolor,
        #                    ls=self.pinf.sch.hlinesstyle,
        #                    lw=self.pinf.sch.hlineswidth)

        #     if self.pinf.sch.legendind and \
        #        ind.plotinfo._get('plotlegend', True):

        #         handles, labels = ax.get_legend_handles_labels()
        #         # Ensure that we have something to show
        #         if labels:
        #             # location can come from the user
        #             loc = ind.plotinfo.legendloc or self.pinf.sch.legendindloc

        #             # Legend done here to ensure it includes all plots
        #             legend = ax.legend(loc=loc,
        #                                numpoints=1, frameon=False,
        #                                shadow=False, fancybox=False,
        #                                prop=self.pinf.prop)

        #             # legend.set_title(indlabel, prop=self.pinf.prop)
        #             # hack: if title is set. legend has a Vbox for the labels
        #             # which has a default "center" set
        #             legend._legend_box.align = 'left'
        
        # plot subindicators on self with independent axis below
        for downind in downinds:
            self.plotind(iref, downind)

        return fig


    def plotdata(self, data, indicators):
        '''
        Creates single bokeh figure for data
        '''

        # initialize tooltips and formatters for data related figure
        # self.dataplottooltips = []
        # self.dataplotformatters = {}

        for ind in indicators:
            upinds = self.dplotsup[ind]
            for upind in upinds:
                self.plotind(data, upind,
                             subinds=self.dplotsover[upind],
                             upinds=self.dplotsup[upind],
                             downinds=self.dplotsdown[upind])

        # opens = data.open.plotrange(self.pinf.xstart, self.pinf.xend)
        # highs = data.high.plotrange(self.pinf.xstart, self.pinf.xend)
        # lows = data.low.plotrange(self.pinf.xstart, self.pinf.xend)
        # closes = data.close.plotrange(self.pinf.xstart, self.pinf.xend)
        # volumes = data.volume.plotrange(self.pinf.xstart, self.pinf.xend)
        self.opens = data.open.array.tolist()
        self.highs = data.high.array.tolist()
        self.lows = data.low.array.tolist()
        self.closes = data.close.array.tolist()
        self.volumes = data.volume.array.tolist()

        self.dataplotsource = ColumnDataSource(data = {
            'date': self.dt_axis,
            'open': self.opens,
            'high': self.highs,
            'low': self.lows,
            'close': self.closes,
            'volume': self.volumes,
        })

        # vollabel = 'Volume'
        pmaster = data.plotinfo.plotmaster
        if pmaster is data:
            pmaster = None

        # voloverlay = (self.pinf.sch.voloverlay and pmaster is None)

        # if not voloverlay:
        #     vollabel += ' ({})'.format(data._dataname)

        # # if self.pinf.sch.volume and self.pinf.sch.voloverlay:
        # axdatamaster = None
        # if self.pinf.sch.volume and voloverlay:
        #     volplot = self.plotvolume(
        #         data, opens, highs, lows, closes, volumes, vollabel)
        #     axvol = self.pinf.daxis[data.volume]
        #     ax = axvol.twinx()
        #     self.pinf.daxis[data] = ax
        #     self.pinf.vaxis.append(ax)
        # else:
        #     if pmaster is None:
        #         ax = self.newaxis(data, rowspan=self.pinf.sch.rowsmajor)
        #     elif getattr(data.plotinfo, 'sameaxis', False):
        #         axdatamaster = self.pinf.daxis[pmaster]
        #         ax = axdatamaster
        #     else:
        #         axdatamaster = self.pinf.daxis[pmaster]
        #         ax = axdatamaster.twinx()
        #         self.pinf.vaxis.append(ax)

        axdatamaster = None # * temporary

        datalabel = ''
        dataname = ''
        if hasattr(data, '_name') and data._name:
            datalabel += data._name

        if hasattr(data, '_compression'):
            print('LOG: compression - %d' % data._compression)
        if hasattr(data, '_timeframe'):
            print('LOG: timeframe - %d' % data._timeframe)

        # candle duration in seconds for '', 'Ticks', 'MicroSeconds', 'Seconds',
        # 'Minutes', 'Days', 'Weeks', 'Months', 'Years', 'NoTimeFrame'
        candle_list = [0, 0.001, 0.001, 1,
                       60, 86400, 604800, 2628000, 31536000, 0]
        candle_sec = candle_list[data._timeframe] * data._compression
        
        print('LOG: candle_sec - %d sec' % candle_sec)

        if hasattr(data, '_compression') and \
           hasattr(data, '_timeframe'):
            tfname = bt.TimeFrame.getname(data._timeframe, data._compression)
            datalabel += ' (%d %s)' % (data._compression, tfname)

        fig = self.new_figure(pwidth=self.pinf.sch.fwidth,
                              pheight=self.pinf.sch.fdheight,
                              ptitle=data._name)

        plinevalues = getattr(data.plotinfo, 'plotlinevalues', True)

        if self.pinf.sch.style.startswith('line'):
            if self.pinf.sch.linevalues and plinevalues:
                datalabel += ' C:%.2f' % self.closes[-1]

            if axdatamaster is None:
                color = self.pinf.sch.loc
            else:
                self.pinf.nextcolor(axdatamaster)
                color = self.pinf.color(axdatamaster)

            self.plot_on_close(fig, color, self.pinf.sch.lwidth, datalabel)

        else:
            if self.pinf.sch.linevalues and plinevalues:
                datalabel += ' O:%.2f H:%.2f L:%.2f C:%.2f' % \
                             (self.opens[-1], self.highs[-1], self.lows[-1],
                              self.closes[-1])

            if self.pinf.sch.style.startswith('candle'):
                self.plot_candlestick(fig,
                    colorup=self.pinf.sch.barup,
                    colordown=self.pinf.sch.bardown,
                    label=datalabel,
                    fillup=self.pinf.sch.barupfill,
                    filldown=self.pinf.sch.bardownfill,
                    candle_width=candle_sec)

            elif self.pinf.sch.style.startswith('bar') or True:
        #         # final default option -- should be "else"
                fig.line(self.dt_axis, closes, legend=datalabel+'_bar',
                         line_width=self.pinf.sch.lwidth, line_color='green')
        #         plotted = plot_ohlc(
        #             ax, self.pinf.xdata, opens, highs, lows, closes,
        #             colorup=self.pinf.sch.barup,
        #             colordown=self.pinf.sch.bardown,
        #             label=datalabel)

        # # Code to place a label at the right hand side with the last value
        # vtags = data.plotinfo._get('plotvaluetags', True)
        # if self.pinf.sch.valuetags and vtags:
        #     self.drawtag(ax, len(self.pinf.xreal), closes[-1],
        #                  facecolor='white', edgecolor=self.pinf.sch.loc)

        # ax.yaxis.set_major_locator(mticker.MaxNLocator(prune='both'))
        # # make sure "over" indicators do not change our scale
        # if data.plotinfo._get('plotylimited', True):
        #     if axdatamaster is None:
        #         ax.set_ylim(ax.get_ylim())

        # if self.pinf.sch.volume:
        #     # if not self.pinf.sch.voloverlay:
        #     if not voloverlay:
        #         self.plotvolume(
        #             data, opens, highs, lows, closes, volumes, vollabel)
        #     else:
        #         # Prepare overlay scaling/pushup or manage own axis
        #         if self.pinf.sch.volpushup:
        #             # push up overlaid axis by lowering the bottom limit
        #             axbot, axtop = ax.get_ylim()
        #             axbot *= (1.0 - self.pinf.sch.volpushup)
        #             ax.set_ylim(axbot, axtop)

        print('LOG: plotdata - data - %s' % (data._name))

        for ind in indicators:
            self.plotind(data, ind, subinds=self.dplotsover[ind], masterax=fig)

        # handles, labels = ax.get_legend_handles_labels()
        # a = axdatamaster or ax
        # if handles:
        #     # put data and volume legend entries in the 1st positions
        #     # because they are "collections" they are considered after Line2D
        #     # for the legend entries, which is not our desire
        #     # if self.pinf.sch.volume and self.pinf.sch.voloverlay:

        #     ai = self.pinf.legpos[a]
        #     if self.pinf.sch.volume and voloverlay:
        #         if volplot:
        #             # even if volume plot was requested, there may be no volume
        #             labels.insert(ai, vollabel)
        #             handles.insert(ai, volplot)

        #     didx = labels.index(datalabel)
        #     labels.insert(ai, labels.pop(didx))
        #     handles.insert(ai, handles.pop(didx))

        #     if axdatamaster is None:
        #         self.pinf.handles[ax] = handles
        #         self.pinf.labels[ax] = labels
        #     else:
        #         self.pinf.handles[axdatamaster] = handles
        #         self.pinf.labels[axdatamaster] = labels
        #         # self.pinf.handles[axdatamaster].extend(handles)
        #         # self.pinf.labels[axdatamaster].extend(labels)

        #     h = self.pinf.handles[a]
        #     l = self.pinf.labels[a]

        #     axlegend = a
        #     loc = data.plotinfo.legendloc or self.pinf.sch.legenddataloc
        #     legend = axlegend.legend(h, l,
        #                              loc=loc,
        #                              frameon=False, shadow=False,
        #                              fancybox=False, prop=self.pinf.prop,
        #                              numpoints=1, ncol=1)

        #     # hack: if title is set. legend has a Vbox for the labels
        #     # which has a default "center" set
        #     legend._legend_box.align = 'left'

        # adding a hover tool to figure
        # fig.add_tools(HoverTool(
        #     tooltips=self.dataplottooltips,
        #     formatters=self.dataplotformatters,
        #     mode='vline'))

        fig.legend.location = self.pinf.sch.legenddataloc
        fig.legend.label_text_font_size = '8pt'
        self.figs.append(fig)

        for ind in indicators:
            downinds = self.dplotsdown[ind]
            for downind in downinds:
                self.plotind(data, downind,
                             subinds=self.dplotsover[downind],
                             upinds=self.dplotsup[downind],
                             downinds=self.dplotsdown[downind])

        # self.pinf.legpos[a] = len(self.pinf.handles[a])

        # if data.plotinfo._get('plotlog', False):
        #     a = axdatamaster or ax
        #     a.set_yscale('log')

        return fig


    def new_figure(self, pwidth=None, pheight=None, ptitle=None,
                   legendloc=None):
        '''
        Creates new bokeh figure
        '''

        main_x_axis = None
        if len(self.figs) != 0:
            main_x_axis = self.figs[0].x_range
            
        fig = figure(x_axis_type="datetime", title=ptitle,
                     plot_width=pwidth, plot_height=pheight,
                     x_range=main_x_axis,
                     toolbar_location=self.pinf.sch.toolbarposition,
                     tools=self.pinf.sch.toolbar)
        
        return fig


    def plot_candlestick(self, fig, colorup, colordown, label,
                         fillup, filldown, candle_width):
        '''
        Create candlestick plot for data
        '''

        w = 0.66*candle_width*1000 # half a bar in ms

        fill_colors, line_colors = [], []
        for o, c in zip(self.opens, self.closes):
            fill_colors.append(fillup*(c>=o)+filldown*(c<o))
            line_colors.append(colorup*(c>=o)+colordown*(c<o))    

        self.dataplotsource.add(fill_colors, 'fcolors')
        self.dataplotsource.add(line_colors, 'lcolors')

        fig.segment(x0='date', y0='high', x1='date', y1='low',
                    source=self.dataplotsource,
                    line_color='lcolors', legend=label)

        fig.vbar(x='date', top='open', bottom='close', width=w,
                 source=self.dataplotsource,
                 fill_color='fcolors', line_color='lcolors')

        # self.dataplottooltips.append(('date', '@date{%F}'))
        # self.dataplotformatters['date'] = 'datetime'
        # self.dataplottooltips.append(('open', '$@{open}{%0.4f}'))
        # self.dataplotformatters['open'] = 'printf'
        # self.dataplottooltips.append(('high', '$@{high}{%0.4f}'))
        # self.dataplotformatters['high'] = 'printf'
        # self.dataplottooltips.append(('low', '$@{low}{%0.4f}'))
        # self.dataplotformatters['low'] = 'printf'
        # self.dataplottooltips.append(('close', '$@{close}{%0.4f}'))
        # self.dataplotformatters['close'] = 'printf'
        # self.dataplottooltips.append(('volume', '$@{volume}{%0.1f}'))
        # self.dataplotformatters['volume'] = 'printf'


    def plot_on_close(self, fig, color, width, label):
        '''
        Create line plot for closes
        '''

        fig.line(x='date', y='close', source=self.dataplotsource,
            legend=label, line_width=width, line_color=color)
        
        # self.dataplottooltips.append(('date', '@date{%F}'))
        # self.dataplotformatters['date'] = 'datetime'
        # self.dataplottooltips.append(('close', '$@{close}{%0.4f}'))
        # self.dataplotformatters['close'] = 'printf'