from unittest.mock import patch

from nose.tools import assert_equal, assert_true, raises
from parameterized import parameterized
from werkzeug.exceptions import HTTPException

from service.platform import Platform
from service.platform.platform_service import create_platform, update_platform


# TODO: adding test to repo.get with none values

@parameterized([
    ({'name': 'ps4'}, True),
    ({'name': 'xbox360'}, True),
    ({'name': '测试'}, True),
    ({'name': 'windows', 'info': '10'}, True),
    ({'name': 'windows', 'info': '10 pro'}, True),
    ({'name': '测试', 'info': '10 测试'}, True),
])
@patch('boto3.resource')
@patch('persistence.platform.PlatformRepository')
def test_create_platform_with_success(request, is_created: bool, boto, repository):
    repository.search.return_value = []
    response = create_platform(request)
    assert_true(response)
    assert_equal('error' not in response.keys(), is_created)
    assert_equal('platformId' in response.keys(), is_created)


@parameterized([
    ({'name': 'xbox360', 'platformId': '123-123'}, False),
    ({'name': 'xbox360', 'platformId': ''}, False),
    ({'name': 'xbox360', 'platformId': None}, False),
    ({'name': 'xbox360', 'modificationDate': 123456}, False),
    ({'name': 'xbox360', 'creationDate': 123456}, False),
    ({'name': ''}, False),
    ({'name': None}, False),
    ({'named': 'windows'}, False),
    ({'named': 'windows', 'info': '10'}, False),
    ({'name': 'windows', 'infos': '10'}, False),
    ({'name': 'windows', 'infos': '10'}, False),
    ({'name': '测试', 'infos': '测试'}, False),
    ({'': 'windows'}, False),
    ({}, False),
    ([], False),
])
@patch('boto3.resource')
@patch('persistence.platform.PlatformRepository')
@raises(HTTPException)
def test_create_platform_with_fail(request, is_created: bool, boto, repository):
    repository.search.return_value = []
    create_platform(request)


@parameterized([
    ({'platformId': '123-123', 'name': 'ps4'}, True),
    ({'platformId': '123-123', 'name': 'xbox360'}, True),
    ({'platformId': '123-123', 'name': '测试'}, True),
    ({'platformId': '123-123', 'name': 'windows', 'info': '10'}, True),
    ({'platformId': '123-123', 'name': 'windows', 'info': '10 pro'}, True),
    ({'platformId': '123-123', 'name': '测试', 'info': '10 测试'}, True),
])
@patch('boto3.resource')
@patch('persistence.platform.PlatformRepository')
def test_update_platform_with_success(request, is_updated: bool, boto, repository):
    repository.search.return_value = []
    repository.get.return_value = Platform(name='name_db', info='type').build_to_create()
    response = update_platform(request)
    assert_true(response)
    assert_equal('error' not in response.keys(), is_updated)
    assert_equal('platformId' in response.keys(), is_updated)
    assert_equal('modificationDate' in response.keys(), is_updated)


@parameterized([
    ({'platformId': '', 'name': 'xbox360'}, False),
    ({'platformId': None, 'name': 'xbox360'}, False),
    ({'platformId': '123-123', 'name': 'xbox360', 'modificationDate': 123456}, False),
    ({'platformId': '123-123', 'name': 'xbox360', 'creationDate': 123456}, False),
    ({'platformId': '123-123', 'name': ''}, False),
    ({'platformId': '123-123', 'name': None}, False),
    ({'platformId': '123-123', 'named': 'windows'}, False),
    ({'platformId': '123-123', 'named': 'windows', 'info': '10'}, False),
    ({'platformId': '123-123', 'name': 'windows', 'infos': '10'}, False),
    ({'platformId': '123-123', 'name': 'windows', 'infos': '10'}, False),
    ({'platformId': '123-123', 'name': '测试', 'infos': '测试'}, False),
    ({'platformId': '123-123', '': 'windows'}, False),
    ({'platformIds': '123-123', 'name': 'windows'}, False),
    ({'platformIds': '123-123', '': 'windows'}, False),
    ({'platformIds': '123-123'}, False),
    ({'platformId': '123-123'}, False),
    ({}, False),
    ([], False),
])
@patch('boto3.resource')
@patch('persistence.platform.PlatformRepository')
@raises(HTTPException)
def test_update_platform_with_fail(request, is_updated: bool, boto, repository):
    repository.search.return_value = []
    repository.get.return_value = Platform(name='name_db', info='type').build_to_create()
    update_platform(request)
