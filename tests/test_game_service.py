from copy import deepcopy

import pytest
from werkzeug.exceptions import HTTPException

from service.game import GameRepository
from service.game_service import create_game, update_game, delete_game
from service.platform import Platform
from tests.base.game_constants import GAME_CREATE_PAYLOAD, GAME_UPDATE_PAYLOAD, INVALID_GAME_PAYLOAD


class TestGame:

    @pytest.fixture
    def platform(self):
        return Platform(name='platform to test', platform_id='1')

    @pytest.mark.parametrize('body', [
        GAME_CREATE_PAYLOAD
    ])
    def test_create_game_with_success(self, body, mocker, platform):
        mocker.patch('boto3.resource')
        search = mocker.patch('service.game.GameRepository.search', return_value=[])
        platform_search = mocker.patch('service.platform.PlatformRepository.search', return_value=[platform])
        platform_get = mocker.patch('service.platform.PlatformRepository.get', return_value=platform)
        save = mocker.patch('service.game.GameRepository.save')
        get = mocker.patch('service.game.GameRepository.get')
        response = create_game(body)
        search.assert_called_once_with(name=body['name'], account=body['account'], validate=True)
        save.assert_called_once_with(game=mocker.ANY)
        assert platform_search.called
        assert platform_get.called
        assert not get.called
        assert response
        assert 'error' not in response.keys()
        assert 'gameId' in response.keys()

    @pytest.mark.parametrize('body', [
        GAME_UPDATE_PAYLOAD
    ])
    def test_delete_game_with_success(self, body, mocker, platform):
        game = GameRepository.build_game(GAME_UPDATE_PAYLOAD)
        mocker.patch('boto3.resource')
        get = mocker.patch('service.game.GameRepository.get',
                           return_value=game)
        delete = mocker.patch('service.game.GameRepository.delete')
        delete_game(account=game.account, game_id=game.game_id)
        get.assert_called_once_with(account=game.account, game_id=game.game_id)
        delete.assert_called_once_with(account=game.account, game_id=game.game_id)

    @pytest.mark.parametrize('body', [
        GAME_UPDATE_PAYLOAD
    ])
    def test_update_game_with_success(self, body, mocker, platform):
        mocker.patch('boto3.resource')
        search = mocker.patch('service.game.GameRepository.search', return_value=[])
        platform_search = mocker.patch('service.platform.PlatformRepository.search', return_value=[platform])
        platform_get = mocker.patch('service.platform.PlatformRepository.get', return_value=platform)
        save = mocker.patch('service.game.GameRepository.save')
        get = mocker.patch('service.game.GameRepository.get')
        response = update_game(body)
        search.assert_called_once_with(name=body['name'], account=body['account'], validate=True)
        save.assert_called_once_with(game=mocker.ANY)
        assert platform_search.called
        assert platform_get.called
        assert get.called
        assert response
        assert 'error' not in response.keys()
        assert 'gameId' in response.keys()

    @pytest.mark.parametrize('body', [
        INVALID_GAME_PAYLOAD,
        GAME_UPDATE_PAYLOAD,
        {},
        [],
        [{'name': 'xbox360'}],
        '',
    ])
    def test_create_game_invalid_body(self, body, mocker):
        mocker.patch('boto3.resource')
        search = mocker.patch('service.game.GameRepository.search')
        get = mocker.patch('service.game.GameRepository.get')
        save = mocker.patch('service.game.GameRepository.save')
        with pytest.raises(HTTPException) as ex:
            create_game(request=body)
        assert not search.called
        assert not save.called
        assert not get.called
        assert 'BadRequest' in str(ex)

    @pytest.mark.parametrize('body', [
        INVALID_GAME_PAYLOAD,
        GAME_CREATE_PAYLOAD,
        {},
        [],
        [{'name': 'xbox360'}],
        '',
    ])
    def test_update_game_invalid_body(self, body, mocker):
        mocker.patch('boto3.resource')
        search = mocker.patch('service.game.GameRepository.search')
        get = mocker.patch('service.game.GameRepository.get')
        save = mocker.patch('service.game.GameRepository.save')
        with pytest.raises(HTTPException) as ex:
            update_game(request=body)
        assert not search.called
        assert not save.called
        assert not get.called
        assert 'BadRequest' in str(ex)

    @pytest.mark.parametrize('body', [
        GAME_CREATE_PAYLOAD
    ])
    def test_create_game_with_conflict(self, body, mocker):
        mocker.patch('boto3.resource')
        payload = deepcopy(GAME_CREATE_PAYLOAD)
        payload['gameId'] = '1'
        search = mocker.patch('service.game.GameRepository.search',
                              return_value=[GameRepository.build_game(payload)])
        get = mocker.patch('service.game.GameRepository.get', return_value=None)
        save = mocker.patch('service.game.GameRepository.save')
        with pytest.raises(HTTPException) as ex:
            create_game(request=body)
        search.assert_called_once_with(name=body['name'], account=body['account'], validate=True)
        assert not save.called
        assert not get.called
        assert 'Conflict' in str(ex)

    @pytest.mark.parametrize('body', [
        GAME_UPDATE_PAYLOAD
    ])
    def test_update_game_with_conflict(self, body, mocker):
        mocker.patch('boto3.resource')
        payload = deepcopy(GAME_CREATE_PAYLOAD)
        payload['gameId'] = '2'
        search = mocker.patch('service.game.GameRepository.search',
                              return_value=[GameRepository.build_game(payload)])
        get = mocker.patch('service.game.GameRepository.get', return_value=None)
        save = mocker.patch('service.game.GameRepository.save')
        with pytest.raises(HTTPException) as ex:
            update_game(request=body)
        search.assert_called_once_with(name=body['name'], account=body['account'], validate=True)
        assert not save.called
        assert not get.called
        assert 'Conflict' in str(ex)

    @pytest.mark.parametrize('body', [
        GAME_UPDATE_PAYLOAD
    ])
    def test_delete_game_not_found(self, body, mocker, platform):
        game = GameRepository.build_game(GAME_UPDATE_PAYLOAD)
        mocker.patch('boto3.resource')
        get = mocker.patch('service.game.GameRepository.get', return_value=None)
        delete = mocker.patch('service.game.GameRepository.delete')
        with pytest.raises(HTTPException) as ex:
            delete_game(account=game.account, game_id=game.game_id)
        get.assert_called_once_with(account=game.account, game_id=game.game_id)
        assert not delete.called
        assert 'Not Found' in str(ex)
