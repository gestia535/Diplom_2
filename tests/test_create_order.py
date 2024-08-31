import allure
import requests
from data import correct_ingredients, CREATE_ORDER, incorrect_ingredients


class TestCreateOrder:

    @allure.title('Проверка успешного создания заказа при отправке корректных данных об ингредиентах '
                  'для авторизованного пользователя')
    @allure.description('Проверка получения кода 200 Ok и сообщения {"success": True} при отправке POST-запроса '
                        'с корректными данными об ингредиентах на создание заказа авторизованного пользователя')
    def test_create_order_with_auth_success(self, create_and_login_user):
        payload, login_response = create_and_login_user
        access_token = login_response.json().get('accessToken')
        order_payload = correct_ingredients
        headers = {'Authorization': f'{access_token}'}
        order_response = requests.post(CREATE_ORDER, json=order_payload, headers=headers)
        assert order_response.status_code == 200 and order_response.json().get('success') is True

    @allure.title('Проверка успешного создания заказа при отправке корректных данных об ингредиентах '
                  'для неавторизованного пользователя')
    @allure.description('Проверка получения кода 200 Ok и сообщения {"success": True} при отправке POST-запроса '
                        'с корректными данными об ингредиентах на создание заказа неавторизованного пользователя')
    def test_create_order_without_auth_success(self):
        order_payload = correct_ingredients
        order_response = requests.post(CREATE_ORDER, json=order_payload)
        assert order_response.status_code == 200 and order_response.json().get('success') is True

    @allure.title('Проверка неудачного создания заказа при отправке запроса без данных по ингредиентам.')
    @allure.description('Проверка получения кода 400 Bad request и сообщения '
                        '{"success": False, "message": "Ingredient ids must be provided"} при отправке POST-запроса '
                        'на создание заказа без указания ингредиентов')
    def test_create_order_without_ingredients_failed(self):
        order_response = requests.post(CREATE_ORDER)
        assert (order_response.status_code == 400 and
                order_response.json() == {'success': False, 'message': 'Ingredient ids must be provided'})

    @allure.title('Проверка неудачного создания заказа при отправке запроса с некорректным хешем ингредиентов.')
    @allure.description('Проверка получения кода 500 Internal Server Error при отправке POST-запроса '
                        'на создание заказа с указанием некорректных хеш-кодов ингредиентов')
    def test_create_order_with_incorrect_hash_failed(self):
        order_payload = incorrect_ingredients
        order_response = requests.post(CREATE_ORDER, json=order_payload)
        assert order_response.status_code == 500 and 'Internal Server Error' in order_response.text
