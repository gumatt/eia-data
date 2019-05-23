import sys
import os
from loguru import logger

from app.services.data_fetcher import SOURCE_URL_KEY, DATA_DIR_KEY
import app.services.data_fetcher as data_fetcher
import eia_config as config
from app.repositories.chart_data import ChartDataRepository, InMemoryChartDataRepository
from app.core.charting import ChartFactory

source_urls = config.source_urls
data_dir = config.data_directory
chart_definitions = config.charts

def render_charts(request):
    repository = InMemoryChartDataRepository(urls=source_urls)
    chart_factory = ChartFactory(repository)
    for definition in chart_definitions:
        logger.info(f'rendering chart definded by {definition}')
        chart_factory.render_chart(definition)
