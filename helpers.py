import requests
import random
import string

from data import DELETE_USER

first_names = ['aleksandr', 'ivan', 'mariya', 'anna', 'dmitriy',
               'ekaterina', 'nikolay', 'olga', 'vladimir', 'natalya']
last_names = ['ivanov', 'petrov', 'smirnov', 'kuznetsov', 'popov',
              'vasiliev', 'pavlov', 'sokolov', 'mikhailov', 'novikov']


def login_generator(domain='gmail.com'):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    number = random.randint(1, 999)
    email = f'{first_name}_{last_name}{number}@{domain}'
    return email


def name_generator():
    user_name = random.choice(first_names)
    return user_name


def password_generator():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=6))
    return password


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


def delete_user(response_data):
    access_token = response_data.json().get('accessToken')
    requests.delete(DELETE_USER, headers={'Authorization': access_token})
