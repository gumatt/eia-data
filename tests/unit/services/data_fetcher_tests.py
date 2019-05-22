import pytest
from assertpy import assert_that

from app.services.data_fetcher import URLDataFetcher, SOURCE_URL_KEY, DATA_DIR_KEY, get_url_list_from_params


@pytest.fixture
def simple_config():
    return {
       'url': 'test url',
        DATA_DIR_KEY: './test_data'
    }

def get_urls_from_params_single_url_test():
    '''Services :: get_urls_from_params :: single url as param'''
    url_list = get_url_list_from_params({'url': 'single url'})

    assert_that(url_list).contains('single url')
    assert_that(url_list).is_equal_to(['single url'])

def get_urls_from_params_no_url_test():
    '''Services :: get_urls_from_params :: no url as param returns empty list'''
    url_list = get_url_list_from_params({})

    assert_that(url_list).is_equal_to([])

def get_urls_from_params_empty_url_list_test():
    '''Services :: get_urls_from_params :: empty urls list as param return empty list'''
    url_list = get_url_list_from_params({'urls': []})

    assert_that(url_list).is_equal_to([])

def get_urls_from_param_url_as_list_test():
    '''Services :: get_urls_from_params :: url param as list returns list'''
    url_list = get_url_list_from_params({'url': ['one url', 'two url', 'three url']})

    assert_that(url_list).contains('three url')
    assert_that(url_list).is_length(3)

def instantiate_URLDataFetcher_test():
    '''Services :: URLDataFetcher :: instantiation tests'''
    assert_that(URLDataFetcher({})).is_not_none
    assert_that(URLDataFetcher({})).is_instance_of(URLDataFetcher)

def URLDataFetcher_add_url_or_dir_to_empty_object_test():
    '''Services :: URLDataFetcher :: updates url or data dir after instantiated empty'''
    fetcher = URLDataFetcher({})
    fetcher.url = 'test url'
    fetcher.data_dir = './data'

    assert_that(fetcher.url).is_equal_to('test url')
    assert_that(fetcher.data_dir).is_equal_to('./data')

def urldatafetcher_url_test(simple_config):
    '''Services :: URLDataFetcher :: source url working'''
    fetcher = URLDataFetcher(simple_config)

    assert_that(fetcher).is_not_none
    assert_that(fetcher.url).is_equal_to(simple_config[SOURCE_URL_KEY])

    fetcher.url = 'second url'
    assert_that(fetcher.url).is_equal_to('second url')

def urldatafetcher_data_dir_test(simple_config):
    '''Services :: URLDataFetcher :: source data_dir working'''
    fetcher = URLDataFetcher(simple_config)

    assert_that(fetcher).is_not_none
    assert_that(fetcher.data_dir).is_equal_to(simple_config[DATA_DIR_KEY])

## TODO: Test that data dir is created if needed
## TODO: Test that destination file name is created accurately
