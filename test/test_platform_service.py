import pytest
from service.platform_service import create_platform
from werkzeug.exceptions import HTTPException


class TestPlatform:

    @pytest.mark.parametrize('body', [
        {'name': 'ps4'},
        {'name': '测试'},
        {'name': '测试', 'info': '10 测试'}
    ])
    def test_create_platform_with_success(self, body, mocker):
        mocker.patch('boto3.resource')
        search = mocker.patch('service.platform.PlatformRepository.search', return_value=[])
        save = mocker.patch('service.platform.PlatformRepository.save')
        get = mocker.patch('service.platform.PlatformRepository.get')
        response = create_platform(body)
        search.assert_called_once_with(name=body['name'], validate=True)
        save.assert_called_once_with(platform=mocker.ANY)
        assert not get.called
        assert response
        assert 'error' not in response.keys()
        assert 'platformId' in response.keys()

    @pytest.mark.parametrize('body', [
        {'name': 'xbox360', 'platformId': '123-123'},
        {'name': ''},
        {},
        [],
        [{'name': 'xbox360'}],
        '',
    ])
    def test_create_platform_invalid_body(self, body, mocker):
        mocker.patch('boto3.resource')
        search = mocker.patch('service.platform.PlatformRepository.search', return_value=[])
        get = mocker.patch('service.platform.PlatformRepository.get', return_value=None)
        save = mocker.patch('service.platform.PlatformRepository.save')
        with pytest.raises(HTTPException) as ex:
            create_platform(request=body)
        assert not search.called
        assert not save.called
        assert not get.called
        assert 'BadRequest' in str(ex)

    @pytest.mark.parametrize('body', [
        {'name': 'platform'},
        {'name': 'platform', 'info': 'info'},
    ])
    def test_create_platform_with_conflict(self, body, mocker):
        mocker.patch('boto3.resource')
        search = mocker.patch('service.platform.PlatformRepository.search', return_value=[{'name': 'platform'}])
        get = mocker.patch('service.platform.PlatformRepository.get', return_value=None)
        save = mocker.patch('service.platform.PlatformRepository.save')
        with pytest.raises(HTTPException) as ex:
            create_platform(request=body)
        search.assert_called_once_with(name=body['name'], validate=True)
        assert not save.called
        assert not get.called
        assert 'Conflict' in str(ex)
