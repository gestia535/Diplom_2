import allure
import requests
from data import GET_ORDERS, correct_ingredients, CREATE_ORDER


class TestsGetUsersOrder:

    @allure.title('Проверка успешного получения заказа пользователя при отправке запроса залогиненого пользователя')
    @allure.description('Проверка получения кода 200 Ok и совпадения параметра "number" в созданном заказе и '
                        'в ответе на запрос при отправке GET-запроса на получение заказов пользователя')
    def test_get_users_order_with_auth_success(self, create_order):
        access_token = create_order[0]
        headers = {'Authorization': access_token}
        get_order_response = requests.get(GET_ORDERS, headers=headers)
        assert get_order_response.status_code == 200 and get_order_response.json().get('success') is True

    @allure.title('Проверка неудачного получения заказа при отправке запроса незалогиненого пользователя')
    @allure.description('Проверка получения кода 401 Not authorized и сообщения '
                        '{"success": False, "message": "You should be authorised"} при отправке GET-запроса '
                        'на получение заказов неавторизованного пользователя')
    def test_get_users_order_without_auth_failed(self):
        order_payload = correct_ingredients
        requests.post(CREATE_ORDER, json=order_payload)
        get_order_response = requests.get(GET_ORDERS)
        assert (get_order_response.status_code == 401 and
                get_order_response.json() == {'success': False, 'message': 'You should be authorised'})
