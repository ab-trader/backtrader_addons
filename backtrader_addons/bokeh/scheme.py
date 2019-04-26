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

from bokeh.palettes import Category10, Inferno

tab10_index = [3, 0, 2, 4, 5, 6, 7, 8, 9, 1]

class PlotScheme(object):

    def __init__(self):

        # * new argument
        # default thickness for all line plots
        self.lwidth = 1.5

        # * new argument
        # layout of the figures: single column of figures (True) similar to
        # baseline backtrader plot or multiple tab layout (False)
        self.btlayout = True

        # * new argument
        # width of the single figure
        self.fwidth = 1200

        # * new argument
        # height of the single data figure
        self.fdheight = 600

        # * new argument
        # height of the single indicator/observer figure
        self.fiheight = 300

        # * new argument
        # set figure toolbar position (per bokeh)
        self.toolbarposition = 'above'

        # * new argument
        # set figure toolbar position (per bokeh)
        self.toolbar = 'pan,wheel_zoom,box_zoom,save,reset'

        # to have a tight packing on the chart wether only the x axis or also
        # the y axis have (see matplotlib)
        self.ytight = False

        # y-margin (top/bottom) for the subcharts. This will not overrule the
        # option plotinfo.plotymargin
        self.yadjust = 0.0
        # Each new line is in z-order below the previous one. change it False
        # to have lines paint above the previous line
        self.zdown = True
        # Rotation of the date labes on the x axis
        self.tickrotation = 15

        # How many "subparts" takes a major chart (datas) in the overall chart
        # This is proportional to the total number of subcharts
        self.rowsmajor = 5

        # How many "subparts" takes a minor chart (indicators/observers) in the
        # overall chart. This is proportional to the total number of subcharts
        # Together with rowsmajor, this defines a proportion ratio betwen data
        # charts and indicators/observers charts
        self.rowsminor = 1

        # Distance in between subcharts
        self.plotdist = 0.0

        # Have a grid in the background of all charts
        self.grid = True

        # * supported only 'line' and 'candle' styles
        # Default plotstyle for the OHLC bars which (line -> line on close)
        # Other options: 'bar' and 'candle'
        self.style = 'line'

        # * supported
        # Default color for the 'line on close' plot
        self.loc = 'black'
        # * supported
        # Default color for a bullish bar/candle
        self.barup = 'black'
        # * supported
        # Default color for a bearish bar/candle
        self.bardown = 'black'
        # Level of transparency to apply to bars/cancles (NOT USED)
        self.bartrans = 1.0

        # * supported
        # Fill colors for candle bars
        self.barupfill = 'white'
        self.bardownfill = 'black'

        # * to be removed
        # Wether the candlesticks have to be filled or be transparent
        self.fillalpha = 0.20

        # Wether to plot volume or not. Note: if the data in question has no
        # volume values, volume plotting will be skipped even if this is True
        self.volume = True

        # * always use separate subchart
        # Wether to overlay the volume on the data or use a separate subchart
        self.voloverlay = True
        # Scaling of the volume to the data when plotting as overlay
        self.volscaling = 0.33
        # Pushing overlay volume up for better visibiliy. Experimentation
        # needed if the volume and data overlap too much
        self.volpushup = 0.00

        # Default colour for the volume of a bullish day
        self.volup = '#aaaaaa'  # 0.66 of gray
        # Default colour for the volume of a bearish day
        self.voldown = '#cc6073'  # (204, 96, 115)
        # Transparency to apply to the volume when overlaying
        self.voltrans = 0.50

        # Transparency for text labels (NOT USED CURRENTLY)
        self.subtxttrans = 0.66
        # Default font text size for labels on the chart
        self.subtxtsize = 9

        # Transparency for the legend (NOT USED CURRENTLY)
        self.legendtrans = 0.25
        # Wether indicators have a leged displaey in their charts
        self.legendind = True
        # * SUPPORTED
        # Location of the legend for indicators (see bokeh)
        self.legendindloc = 'top_left'
        # * SUPPORTED
        # Location of the legend for datafeeds (see matplotlib)
        self.legenddataloc = 'top_left'

        # Plot the last value of a line after the Object name
        self.linevalues = True

        # Plot a tag at the end of each line with the last value
        self.valuetags = True

        # Default color for horizontal lines (see plotinfo.plothlines)
        self.hlinescolor = '0.66'  # shade of gray
        # Default style for horizontal lines
        self.hlinesstyle = '--'
        # Default width for horizontal lines
        self.hlineswidth = 1.0

        # * UPDATED
        # Default color scheme: Category10
        self.lcolors = Category10[10]

        # strftime Format string for the display of ticks on the x axis
        self.fmt_x_ticks = None

        # strftime Format string for the display of data points values
        self.fmt_x_data = None


    def color(self, idx):
        colidx = tab10_index[idx % len(tab10_index)]
        return self.lcolors[colidx]


    def translate_marker(self, mpl_marker):
        '''
        Translate matplotlib marker to bokeh marker
        '''
        mpl_markers = ['o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's',
                       'p', '*', 'h', 'H', '+', 'x', 'D', 'd']
        b_markers = ['circle', 'inverted_triangle', 'triangle', 'circle_x.nf',
                     'circle_cross.nf', 'triangle.nf', 'inverted_triangle.nf',
                     'circle.nf', 'square_cross.nf', 'square', 'square.nf',
                     'square_x.nf', 'asterisk', 'hex.nf', 'hex', 'cross', 'x',
                     'diamond', 'diamond_cross.nf']
        if mpl_marker in mpl_markers:
            mf = b_markers[mpl_markers.index(mpl_marker)].split('.')
        else:
            mf = ['asterisk']
        marker = mf[0]
        fill = (len(mf) == 1)

        return marker, fill


    def translate_color(self, mpl_color):
        '''
        Translate matplotlib color to bokeh color
        '''
        mpl_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k',
                      'lime', 'red', 'blue', 'grey', 'green', 'black'] 
        b_colors =['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black',
                   'lime', 'red', 'blue', 'grey', 'green', 'black']
        if mpl_color in mpl_colors:
            color = b_colors[mpl_colors.index(mpl_color)]
        else:
            color = 'blue'        

        return color