import pytest
from assertpy import assert_that

from app.services.data_fetcher import URLDataFetchService, SOURCE_URL_KEY, DATA_DIR_KEY


@pytest.fixture
def simple_config():
    return {
        'urls': [
            'test_url1',
            'test_url2',
            'test_url3'
        ],
        DATA_DIR_KEY: './test_data'
    }


def instantiate_URLDataFetcher_test():
    '''Services :: URLDataFetchService :: instantiation tests'''
    assert_that(URLDataFetchService({})).is_not_none
    assert_that(URLDataFetchService({})).is_instance_of(URLDataFetchService)


