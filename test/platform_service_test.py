from unittest.mock import patch

from nose.tools import assert_equal, assert_true
from parameterized import parameterized

from persistence.platform import Platform
from service.platform_service import create_platform, update_platform


@parameterized([
    ({'name': 'ps4'}, True),
    ({'name': 'xbox360'}, True),
    ({'name': '测试'}, True),
    ({'name': 'windows', 'subtype': '10'}, True),
    ({'name': 'windows', 'subtype': '10 pro'}, True),
    ({'name': '测试', 'subtype': '10 测试'}, True),
    ({'name': 'xbox360', 'platformId': '123-123'}, False),
    ({'name': 'xbox360', 'platformId': ''}, False),
    ({'name': 'xbox360', 'platformId': None}, False),
    ({'name': 'xbox360', 'modificationDate': 123456}, False),
    ({'name': 'xbox360', 'creationDate': 123456}, False),
    ({'name': ''}, False),
    ({'name': None}, False),
    ({'named': 'windows'}, False),
    ({'named': 'windows', 'subtype': '10'}, False),
    ({'name': 'windows', 'subtypes': '10'}, False),
    ({'name': 'windows', 'subtypes': '10'}, False),
    ({'name': '测试', 'subtypes': '测试'}, False),
    ({'': 'windows'}, False),
    ({}, False),
    ([], False),
])
def test_create_platform(request, is_created: bool):
    response = create_platform(request)
    assert_true(response)
    assert_equal('error' not in response.keys(), is_created)
    assert_equal('platformId' in response.keys(), is_created)


@parameterized([
    ({'platformId': '123-123', 'name': 'ps4'}, True),
    ({'platformId': '123-123', 'name': 'xbox360'}, True),
    ({'platformId': '123-123', 'name': '测试'}, True),
    ({'platformId': '123-123', 'name': 'windows', 'subtype': '10'}, True),
    ({'platformId': '123-123', 'name': 'windows', 'subtype': '10 pro'}, True),
    ({'platformId': '123-123', 'name': '测试', 'subtype': '10 测试'}, True),
    ({'platformId': '', 'name': 'xbox360'}, False),
    ({'platformId': None, 'name': 'xbox360'}, False),
    ({'platformId': '123-123', 'name': 'xbox360', 'modificationDate': 123456}, False),
    ({'platformId': '123-123', 'name': 'xbox360', 'creationDate': 123456}, False),
    ({'platformId': '123-123', 'name': ''}, False),
    ({'platformId': '123-123', 'name': None}, False),
    ({'platformId': '123-123', 'named': 'windows'}, False),
    ({'platformId': '123-123', 'named': 'windows', 'subtype': '10'}, False),
    ({'platformId': '123-123', 'name': 'windows', 'subtypes': '10'}, False),
    ({'platformId': '123-123', 'name': 'windows', 'subtypes': '10'}, False),
    ({'platformId': '123-123', 'name': '测试', 'subtypes': '测试'}, False),
    ({'platformId': '123-123', '': 'windows'}, False),
    ({'platformIds': '123-123', 'name': 'windows'}, False),
    ({'platformIds': '123-123', '': 'windows'}, False),
    ({'platformIds': '123-123'}, False),
    ({'platformId': '123-123'}, False),
    ({}, False),
    ([], False),
])
@patch('persistence.platform.PlatformRepository.get')
def test_update_platform(request, is_updated: bool, get):
    get.return_value = Platform(name='name_db', subtype='type').build_to_create()
    response = update_platform(request)
    assert_true(response)
    assert_equal('error' not in response.keys(), is_updated)
    assert_equal('platformId' in response.keys(), is_updated)
    assert_equal('modificationDate' in response.keys(), is_updated)

# TODO: adding test to repo.get with none values
