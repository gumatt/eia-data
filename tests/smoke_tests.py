from assertpy import assert_that

def pytest_smoke_test():
    ''' Infra dev :: pytest :: smoke_tests::assert true passes'''
    assert True

def assertpy_smoke_test():
    ''' Infra dev :: pytest ::smoke_tests::assertpy module working'''
    assert_that('').is_not_none()
    assert_that('').is_empty()
    assert_that('').is_false()
    assert_that('').is_type_of(str)
    assert_that('').is_instance_of(str)