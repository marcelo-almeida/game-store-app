import pytest
from service.platform_service import create_platform
from werkzeug.exceptions import HTTPException


@pytest.mark.parametrize('body', [
    {'name': 'ps4'},
    {'name': '测试'},
    {'name': '测试', 'info': '10 测试'}
])
def test_create_platform_with_success(body, mocker):
    mocker.patch('boto3.resource')
    mocker.patch('service.platform.PlatformRepository.search', return_value=[])
    mocker.patch('service.platform.PlatformRepository.save')
    response = create_platform(body)
    assert response
    assert 'error' not in response.keys()
    assert 'platformId' in response.keys()


@pytest.mark.parametrize('body', [
    ({'name': 'xbox360', 'platformId': '123-123'})
])
def test_create_platform_with_fail(body, mocker):
    mocker.patch('boto3.resource')
    mocker.patch('service.platform.PlatformRepository.search', return_value=[])
    mocker.patch('service.platform.PlatformRepository.get', return_value=None)
    with pytest.raises(HTTPException):
        create_platform(request=body)
