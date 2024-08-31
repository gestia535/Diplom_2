from helpers import login_generator, password_generator, name_generator
import allure
import pytest
import requests

from data import UPDATE_USER_DATA


class TestsChangeUserData:

    @allure.title('Проверка успешного обновления информации залогиненного пользователя')
    @allure.description('Проверка получения кода 200 Ok и сообщения {"success": True} при отправке PATCH-запроса '
                        'на обновление email, password, name параметров залогиненного пользователя')
    @pytest.mark.parametrize("update_field, new_value", [
        ("email", login_generator()),
        ("password", password_generator()),
        ("name", name_generator())
    ])
    def test_update_data_with_auth_success(self, create_and_login_user, update_field, new_value):
        payload, login_response = create_and_login_user
        access_token = login_response.json().get('accessToken')
        update_payload = {update_field: new_value}
        headers = {'Authorization': f'{access_token}'}
        response = requests.patch(UPDATE_USER_DATA, json=update_payload, headers=headers)
        assert response.status_code == 200 and response.json().get('success') is True

    @allure.title('Проверка неудачного обновления информации незалогиненного пользователя')
    @allure.description('Проверка получения кода 401 Unauthorized и сообщения '
                        '{"success": False, "message": "You should be authorised"} при отправке PATCH-запроса '
                        'на обновление данных полей email, password, name незалогиненного пользователя')
    @pytest.mark.parametrize("update_field, new_value", [
        ("email", login_generator()),
        ("password", password_generator()),
        ("name", name_generator())
    ])
    def test_update_data_without_auth_failed(self, update_field, new_value):
        update_payload = {update_field: new_value}
        response = requests.patch(UPDATE_USER_DATA, json=update_payload)
        assert (response.status_code == 401 and
                response.json() == {'success': False, 'message': 'You should be authorised'})
