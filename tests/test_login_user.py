from helpers import login_generator, password_generator, generate_random_string
import allure
import pytest
import requests

from data import LOGIN_USER


class TestLoginUser:

    @allure.title('Проверка успешной авторизации пользователя при заполненных обязательных полях')
    @allure.description('Проверка получения кода 200 Ok и получения accessToken при отправке POST-запроса '
                        'на авторизацию пользователя при заполненных полях email, password валидными данными')
    def test_login_user_success(self, create_user):
        payload = create_user[0]
        response = requests.post(LOGIN_USER, json=payload)
        assert response.status_code == 200 and 'accessToken' in response.json()

    @allure.title('Проверка неудачного логина пользователя при некорректно заполненных обязательных полях')
    @allure.description('Проверка получения кода 401 Unauthorized и сообщения '
                        '{"success": False, "message": "email or password are incorrect"} при отправке POST-запроса '
                        'на авторизацию пользователя при некорректном email и password')
    @pytest.mark.parametrize('email, password', [
        (generate_random_string(4), password_generator()),
        (login_generator(), generate_random_string(3))
    ])
    def test_login_incorrect_data_failed(self, email, password):
        payload = {'email': email, 'password': password}
        response = requests.post(LOGIN_USER, json=payload)
        assert (response.status_code == 401 and
                response.json() == {'success': False, 'message': 'email or password are incorrect'})
