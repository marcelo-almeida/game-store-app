from nose.tools import assert_equal
from parameterized import parameterized

from service.platform_service import create_platform


@parameterized([
    ({'name': 'ps4'}, True),
    ({'name': 'xbox360'}, True),
    ({'name': 'windows', 'subtype': '10'}, True),
    ({'name': 'windows', 'subtype': '10 pro'}, True),
    ({'name': ''}, False),
    ({'named': 'windows'}, False),
    ({'named': 'windows', 'subtype': '10'}, False),
    ({'name': 'windows', 'subtypes': '10'}, False),
    ({'name': 'windows', 'subtypes': '10'}, False),
    ({'': 'windows'}, False),
    ({}, False),
    ([], False),
])
def test_create_platform(request, is_created: bool):
    response = create_platform(request)
    assert_equal(response is not None, is_created)
    assert_equal(response.get('platformId'), is_created)
