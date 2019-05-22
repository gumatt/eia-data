from datetime import datetime
import jsonplus as json

import pytest
from assertpy import assert_that

from app.core.base import BaseObject


@pytest.fixture
def data_dict():
    return {
        'a': [1, 2, 3], 
        'd': datetime(2018, 10, 3, 21, 24, 13, 495705), 
        'e': [
            'one', 
            'two', 
            'elephant'
            ],
        'name': 'Bob'
        }

@pytest.fixture
def data_dict_w_dict_member():
    return {
        'a': {
            'a': 'a.a',
            'b': 2,
            'c': [1, 2, 3]
        }
    }

@pytest.fixture
def data_str():
    return '{"a":[1,2,3],"d":{"__class__":"datetime","__value__":"2018-10-03T21:24:13.495705"},"e":["one","two","elephant"], "name": "Bob"}'

def instantiate_base_object_test():
    '''Core :: BaseObject :: instantiation tests'''
    assert_that(BaseObject({})).is_not_none
    assert_that(BaseObject.from_json('{}')).is_instance_of(BaseObject)

def check_fixture_test(data_dict):
    '''Core :: BaseObject :: check that fixture working'''
    assert_that(data_dict).is_instance_of(dict)

def instantiate_base_object_from_dict_test(data_dict):
    '''Core :: BaseObject :: can instantiate object from dict and access key as property'''
    bo = BaseObject.from_dict(data_dict)

    assert_that(bo).contains_key('a')
    assert_that(bo.a).is_equal_to([1, 2, 3])
    assert_that(bo.d).is_instance_of(datetime)
    assert_that(bo.d).is_equal_to(data_dict['d'])

def instantiate_base_object_from_dict_within_dict_test(data_dict_w_dict_member):
    '''Core :: BaseObject :: can instantiate object from dict with an embedded dict and access property'''
    data_dict = data_dict_w_dict_member
    bo = BaseObject.from_dict(data_dict)

    assert_that(bo).contains_key('a')
    bo2 = bo.a
    assert_that(bo2.a).is_equal_to('a.a')
    assert_that(bo2.b).is_equal_to(2)
    assert_that(bo2.c).is_equal_to([1, 2, 3])
    assert_that(bo.a.a).is_equal_to(bo2.a)

def instantiate_base_object_from_json_str_test(data_dict, data_str):
    '''Core :: BaseObject :: can instantiate object from json string '''
    bo = BaseObject.from_json(data_str)

    assert_that(bo).contains_key('a')
    assert_that(bo.a).is_equal_to(data_dict['a'])
    assert_that(bo.d).is_instance_of(datetime)
    assert_that(bo.d.day).is_equal_to(3)
    assert_that(bo.d).is_equal_to(data_dict['d'])
