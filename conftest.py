import pytest
import requests

from data import CREATE_USER, DELETE_USER, LOGIN_USER, correct_ingredients, CREATE_ORDER
from helpers import login_generator, password_generator, name_generator


@pytest.fixture()
def create_user():
    payload = {
        'email': login_generator(),
        'password': password_generator(),
        'name': name_generator()
    }
    response = requests.post(CREATE_USER, json=payload)
    response_data = response.json()
    yield payload, response_data
    access_token = response_data['accessToken']
    requests.delete(DELETE_USER, headers={'Authorization': access_token})


@pytest.fixture()
def create_and_login_user():
    payload = {'email': login_generator(), 'password': password_generator(), 'name': name_generator()}
    requests.post(CREATE_USER, json=payload)
    login_response = requests.post(LOGIN_USER, json=payload)
    token = login_response.json().get('accessToken')
    yield payload, login_response
    access_token = token
    requests.delete(DELETE_USER, headers={'Authorization': access_token})


@pytest.fixture()
def create_login_and_order():
    payload = {'email': login_generator(), 'password': password_generator(), 'name': name_generator()}
    requests.post(CREATE_USER, json=payload)
    login_response = requests.post(LOGIN_USER, json=payload)
    access_token = login_response.json().get('accessToken')
    order_payload = correct_ingredients
    headers = {'Authorization': f'{access_token}'}
    order_response = requests.post(CREATE_ORDER, json=order_payload, headers=headers)
    yield login_response, order_response
    requests.delete(DELETE_USER, headers={'Authorization': access_token})
