import os

import pandas as pd
from loguru import logger

import app.services.data_fetcher as data_fetcher


DEFAULT_URLS = [
    'http://ir.eia.gov/wpsr/psw01.xls',
    'http://ir.eia.gov/wpsr/psw02.xls',
    'http://www.eia.gov/dnav/pet/hist_xls/W_EPC0_SAX_YCUOK_MBBLw.xls',
    'http://www.eia.gov/dnav/pet/xls/PET_SUM_SNDW_DCUS_NUS_W.xls'
]

class ChartDataRepository(object):
    def __init__(self, data_dir='./data', raw_data_filenames=['psw01.xls', 'psw02.xls', 'W_EPC0_SAX_YCUOK_MBBLw.xls', 'PET_SUM_SNDW_DCUS_NUS_W.xls']):
        self.data_dir = data_dir
        self.raw_data_filenames = raw_data_filenames
        self.data = None

    @property
    def filenames(self):
        result = []
        for name in self.raw_data_filenames:
            result.append(self.data_dir + '/' + name)
        return result

    def _refresh_repository(self):
        if len(self.raw_data_filenames) > 0:
            self.data = data_fetcher.read_eia_data_from_sources(self.filenames)

    def get_timeseries_dataframe(self, source, sheet):
        if not self.data:
            self._refresh_repository()
        if self.data:
            return self.data[source][sheet]
        else:
            return None

    def get_data(self, source, descriptor):
        return self.get_timeseries_dataframe(source, descriptor)



class InMemoryChartDataRepository(object):
    def __init__(self, urls=DEFAULT_URLS):
        self.raw_data_urls = urls
        self.data = {}

    @property
    def filenames(self):
        result = []
        for url in self.raw_data_urls:
            result.append(os.path.basename(url))
        return result

    def _refresh_repository(self):
        if len(self.raw_data_urls) > 0:
            for url in self.raw_data_urls:
                logger.info(f'retrieving data file from {url}')
                self.data[os.path.basename(url)] = pd.ExcelFile(url)

    def get_timeseries_dataframe(self, source, sheet):
        if not self.data:
            self._refresh_repository()
        if self.data:
            logger.debug(f'repo.data={self.data}')
            xls = self.data[source]
            logger.debug(f'current ExcelFile is {xls}')
            df = xls.parse(sheet, skiprows=[0,2])
            logger.debug(f'dataframe for {sheet} is {df}')
            # clean up columns
            df.rename(columns={'Sourcekey': 'Date'}, inplace=True)
            if 'Date' in df:
                df['Year'] = df['Date'].dt.year
                df['Week'] = df['Date'].dt.week
            return df
        else:
            return None

    def get_data(self, source, descriptor):
        source = os.path.basename(source)
        logger.debug(f'getting repo data from source={source} and sheet={descriptor}')
        return self.get_timeseries_dataframe(source, descriptor)