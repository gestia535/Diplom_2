import allure
import pytest
import requests
from data import CREATE_USER, existing_user_data, DELETE_USER
from helpers import login_generator, password_generator, name_generator


class TestCreateUser:

    @allure.title('Проверка успешной регистрации пользователя при заполненных обязательных полях')
    @allure.description('Проверка получения кода 200 Ok и сообщения {success": True} при отправке POST-запроса '
                        'на регистрацию пользователя при заполненных полях email, password и name валидными данными. '
                        'После теста аккаунт удаляется')
    def test_create_new_user_success(self):
        payload = {'email': login_generator(), 'password': password_generator(), 'name': name_generator()}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(CREATE_USER, json=payload, headers=headers)
        assert response.status_code == 200 and response.json().get('success') is True
        access_token = response.json().get('accessToken')
        requests.delete(DELETE_USER, headers={'Authorization': access_token})

    @allure.title('Проверка неудачной регистрации уже зарегистрированного пользователя')
    @allure.description('Проверка получения кода 403 Forbidden и сообщения '
                        '{"success": False, "message": "User already exists"} при отправке POST-запроса '
                        'на регистрацию уже зарегистрированного пользователя')
    def test_create_existing_user_failed(self):
        payload = existing_user_data
        headers = {'Content-Type': 'application/json'}
        requests.post(CREATE_USER, json=payload, headers=headers)
        response_check = requests.post(CREATE_USER, json=payload, headers=headers)
        assert (response_check.status_code == 403 and
                response_check.json() == {'success': False, 'message': 'User already exists'})

    @allure.title('Проверка неудачной регистрации пользователя при незаполненных обязательных полях')
    @allure.description('Проверка получения кода 403 Forbidden и сообщения '
                        '{"success": False, "message": "Email, password and name are required fields"} '
                        'при отправке POST-запроса '
                        'на регистрацию пользователя при незаполненных полях email/password/name')
    @pytest.mark.parametrize('email, password, name', [
        ('', password_generator(), name_generator()),
        (login_generator(), '', name_generator()),
        (login_generator(), password_generator(), ''),
        ('', '', '')
    ])
    def test_create_user_without_required_fields_failed(self, email, password, name):
        payload = {'email': email, 'password': password, 'name': name}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(CREATE_USER, json=payload, headers=headers)
        assert (response.status_code == 403 and
                response.json() == {'success': False, 'message': "Email, password and name are required fields"})
