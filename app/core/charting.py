''' charting.py

This module contains the basic chart classes [Chart, MultiYearDataTrendChart] that
can be instantiated to produce the EIA charts used on the Powerhouse web site. 
(www.powerhousetl.com/eia-data/)

Todos:
    
'''
from datetime import datetime

import pandas as pd
from plotly.plotly import plot
import plotly.graph_objs as go
from loguru import logger

class ChartFactory(object):
    def __init__(self, repository=None):
        self.repo = repository

    def _get_data(self, source_file, source_sheet, data_id):
        df = self.repo.get_data(source_file, source_sheet)
        if not df is None:
            # date of last data point is in last row of data columns in EIA source data files
            logger.debug(f'repo.get_data({source_file}, {source_sheet}) = {df.head()}')
            self.chart_date = df.iloc[-1]['Date']
            start_year = self.chart_date.year - self.num_years
            start_week = 1
            df['offset'] = 0
            df.loc[df['Week'] >= 53, 'offset'] = -1
            df['Year'] = df['Year'] + df['offset']
            df[data_id] = df[data_id] * self.scale
            df = df.drop(columns=['offset'])
            df = df[['Date', 'Year', 'Week', data_id]].loc[(df['Year'] >= start_year) & (df['Week'] >= start_week)]
            pivoted_data = df.pivot(index='Week', columns='Year', values=data_id)
            pivoted_data['Avg'] = pivoted_data.mean(axis=1)
            pivoted_data['Max'] = pivoted_data.max(axis=1)
            pivoted_data['Min'] = pivoted_data.min(axis=1)
            df = pd.DataFrame(pivoted_data.to_records())
            df = df[ df['Week'] <= 52 ]
        return df

    def render_chart(self, chart_specs):
        #  set chart specs
        logger.debug('chart specs to render: \n {specs}', specs=chart_specs)
        self.num_years = chart_specs.get('num_years', 5)
        self.scale = chart_specs.get('data_scale_factor', 1)
        self.y_axis_name = chart_specs.get('yaxis_name', 'Millions')

        # get and shape chart data
        self.chart_data = self._get_data(chart_specs.get('data_file', None), chart_specs.get('data_sheet', None), chart_specs.get('data_id', None))
        logger.debug('chart data is \n {data}', data=self.chart_data.head(5))

        # define and render chart
        max_line = go.Scatter(
            y = self.chart_data['Max'],
            x = self.chart_data['Week'],
            name = ' '.join([str(self.num_years), chart_specs.get('timeframe_unit', 'Year'), 'Max']),
            fill = None,
            line = {
                'color': '#1F4899'
            }
        )

        min_line = go.Scatter(
            y = self.chart_data['Min'],
            x = self.chart_data['Week'],
            name = ' '.join([str(self.num_years), chart_specs.get('timeframe_unit', 'Year'), 'Min']),
            fill = 'tonexty',
            fillcolor = '#FFEEC5',
            mode = 'lines',
            line = {
                'color': '#1F4899'
            }
        )

        avg_line = go.Scatter(
            y = self.chart_data['Avg'],
            x = self.chart_data['Week'],
            name = ' '.join([str(self.num_years), chart_specs.get('timeframe_unit', 'Year'), 'Avg']),
            line = {
                'color' : '#BAB9BB',
                'width' : 3,
                'dash'  : 'dashdot'
            }
        )

        curr_line = go.Scatter(
            y = self.chart_data[str(self.chart_date.year)],
            x = self.chart_data['Week'],
            name = str(self.chart_date.year),
            line = {
                'color' : '#238C2C',
                'width' : 4
            }
        )

        prev_line = go.Scatter(
            y = self.chart_data[str(self.chart_date.year - 1)],
            x = self.chart_data['Week'],
            name = str(self.chart_date.year - 1),
            line = {
                'color' : '#8BAE44',
                'width' : 4
            }
        )

        # layout should be changed based on ChartType (e.g. MultiYearDataTrendChart, DailyChart, etc)
        layout = go.Layout(
            title = chart_specs.get('title', 'No Title ') + self.chart_date.strftime('%m/%d/%Y'),
            margin = {
                'autoexpand': True,
            },
            images=[{
                'source': "https://powerhousetl.com/wp-content/uploads/logo.gif",
                'visible': True,
                'layer': 'above',
                'sizing': 'contain',
                'xref': "paper", 
                'yref': "paper",
                'x':    1, 
                'y':    0,
                'sizex': 0.2, 
                'sizey': 0.2,
                'xanchor': "left", 
                'yanchor': "bottom"
            }],
            annotations=[{
                'text': 'Source: POWERHOUSE Research, EIA',
                'showarrow': False,
                'xref': 'paper',
                'yref': 'paper',
                'xanchor': 'left',
                'yanchor': 'bottom',
                'x': -0.05,
                'y': -0.2,
                'font': {
                    'size': 11,
                    'color': 'darkgrey',
                }
            }],
            xaxis = {
                'title' : 'Week',
                'automargin': True,
                'titlefont' : {
                    'size' : 16,
                    'color' : 'black'
                },
                'ticks' : 'outside',
                'tick0' : 1,
                'tickvals' : [3, 7, 12, 16, 20, 24, 28, 33, 37, 42, 46, 50],
                'ticktext' : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },
            yaxis={
                'title': self.y_axis_name,
                'automargin': True,
                'titlefont': {
                    'size': 16,
                    'color': 'black'
                }
            }
        )

        chart_data = [max_line, min_line, avg_line, prev_line, curr_line]
        chart = go.Figure(data=chart_data, layout=layout)
        plot(chart, filename = chart_specs.get('name', 'ChartX'), auto_open=chart_specs.get('auto_open', False))  