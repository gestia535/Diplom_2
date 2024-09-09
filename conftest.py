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
def create_order(create_user):
    access_token = create_user[1]['accessToken']
    headers = {'Authorization': access_token}
    payload = correct_ingredients
    response_body = requests.post(CREATE_ORDER, json=payload, headers=headers)
    yield access_token, response_body
