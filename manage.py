import sys
import os
from loguru import logger

from app.services.data_fetcher import SOURCE_URL_KEY, DATA_DIR_KEY
import app.services.data_fetcher as data_fetcher
import eia_config as config
from app.repositories.chart_data import ChartDataRepository, InMemoryChartDataRepository
from app.core.charting import ChartFactory

logger.remove()
logger.add(sys.stdout, level="INFO")
logger.level('INFO', color='<blue>')
source_urls = config.source_urls
data_dir = config.data_directory
chart_definitions = config.charts

# filenames = []
# raw_data_files = []
# for url in source_urls:
#     raw_data_files.append(data_dir+'/'+os.path.basename(url))
#     filenames.append(os.path.basename(url))
# logger.debug('raw data files {files}', files=raw_data_files)
# logger.debug('filenames {filenames}', filenames=filenames)
# data_fetcher.get_data({DATA_DIR_KEY: data_dir, 'urls': source_urls})

# repository = ChartDataRepository(data_dir=data_dir, raw_data_filenames=filenames)
repository = InMemoryChartDataRepository(urls=source_urls)
# logger.debug('chart data for psw01 Data1: \n {data}', data=repository.get_data('psw01.xls', 'Data 1'))

chart_factory = ChartFactory(repository)
for definition in chart_definitions:
    logger.info(f'rendering chart defined by {definition}')
    chart_factory.render_chart(definition)
