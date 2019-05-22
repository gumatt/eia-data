import os
import wget
import pandas as pd
from loguru import logger

from app.core.base import BaseObject

SOURCE_URL_KEY = 'url'
DATA_DIR_KEY = 'data_dir'

def get_data(params):
    urls = get_url_list_from_params(params)
    data_dir = params.get(DATA_DIR_KEY, './data')
    fetcher = URLDataFetcher({DATA_DIR_KEY: data_dir})
    for url in urls:
        logger.info('fetching data from {url} writing to {dir}', url=url, dir=fetcher.data_dir)
        fetcher.url = url
        fetcher.get_data()


def read_eia_data_from_sources(filenames=['./data/psw01.xls']):
    ''' Given a list of file names read them into pandas dataframes 
    
    Keyword Arguments:
        filenames {list} -- list of EIA Weekly data excel spreadsheets (default: {['./data/psw01.xls']})
    
    Returns:
        {dict} -- { file_basename: { sheetname: pd.dataframe }}
                    e.g.   
                    { 'psw01.xls' : {
                        'Contents' : <pd.dataframe>,
                        'Data 1' : <pd.dataframe>
                    }}
    '''
    result = {}
    for source_file in filenames:
        xl = pd.ExcelFile(source_file)
        base_filename = os.path.basename(source_file)
        # print (xl.sheet_names)
        dfs = {sheet: xl_sheet_to_dataframe(xl, sheet) for sheet in xl.sheet_names}
        result[base_filename] = dfs
    return result


def xl_sheet_to_dataframe(xl, sheet):
    '''convert an EIA spreadsheet from an pandas xl file object to a dataframe. This function
        assumes that the spreadsheet is in the form of one of the weekly EIA petroleum
        spreadsheets.  A 'Week' column will be added to the dataframe indicating
        the numerical week of the year for each row.
    
    Arguments:
        xl {object} -- a pandas ExcelFile object
        sheet {string} -- name of the sheet within the xl file to parse
    
    Returns:
        pandas.dataframe -- columns = 'Date', 'Week', 'Year', [items from row 2 of the sheet
                                        i.e. data element short names];
                            rows = data rows from sheet starting at row 4
                            Note:  columns will be in proper data types (e.g. Dates
                                    are datetime objects)
    '''
    df = xl.parse(sheet, skiprows=[0,2])

    # clean up columns
    df.rename(columns={'Sourcekey': 'Date'}, inplace=True)
    if 'Date' in df:
        df['Year'] = df['Date'].dt.year
        df['Week'] = df['Date'].dt.week
    return df


def get_url_list_from_params(params):
    urls = params.get('urls', params.get('url', []))
    if not isinstance(urls, list):
        urls = [urls]
    return urls


class URLDataFetcher(BaseObject):
    download = wget.download

    def update_config(self, config):
        self.url = config.get(SOURCE_URL_KEY, self.url)
        self.data_dir = config.get(DATA_DIR_KEY, self.data_dir)

    def get_data(self, config=None):
        if config:
            self.update_config(config)
        if not os.path.isdir(self.data_dir):
            os.mkdir(self.data_dir)
        new_filename = self.data_dir+'/'+os.path.basename(self.url)
        if os.path.exists(new_filename):
            logger.debug('{filename} exists, removing file', filename=new_filename)
            os.remove(new_filename)
        return wget.download(self.url, self.data_dir+'/'+os.path.basename(self.url), bar=None)



class URLDataFetchService(object):
    def __init__(self, params=None):
        self.fetcher = URLDataFetcher({})
        self.init_fetcher(params)

    def init_fetcher(self, params):
        self.data_dir = params.get(DATA_DIR_KEY, './data')
        self.urls = get_url_list_from_params(params)
        
    def get_data(self, params):
        self.init_fetcher(params)
        self.fetcher.data_dir = self.data_dir
        for url in self.urls:
            self.fetcher.url = url
            self.fetcher.get_data()
        

