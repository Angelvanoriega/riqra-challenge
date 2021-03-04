import pytest
import requests


def test_reset_db():
    response = requests.get(
        'http://3.84.254.116:5000/api/v1/resources/reset_db'
    )
    response = response.json()
    assert (response['message'] == 'Database restablished')
    print('ok reset db')


def test_auto_sign_up():
    response = requests.post(
        'http://3.84.254.116:5000/api/v1/resources/login',
        data={
            'email': 'angel.diaz@live.com.mx',
            'password': '1234567890'
        }
    )
    assert (response.status_code == 200)
    response = response.json()
    assert ('token' in response)
    assert ('supplier_id' in response)
    assert (response['message'] == 'user_signed_up')
    print('ok signup')


def test_login_password_incorrect():
    response = requests.post(
        'http://3.84.254.116:5000/api/v1/resources/login',
        data={
            'email': 'angel.diaz@live.com.mx',
            'password': '0987654321'
        }
    )
    response = response.json()
    code = response['code']
    error = response['error']
    assert (code == 'P0001')
    assert ('Oops! wrong password' in error)
    print('ok login wrong password')


def test_login_correctly():
    response = requests.post(
        'http://3.84.254.116:5000/api/v1/resources/login',
        data={
            'email': 'angel.diaz@live.com.mx',
            'password': '1234567890'
        }
    )
    assert (response.status_code == 200)
    response = response.json()
    assert ('token' in response)
    assert ('supplier_id' in response)
    assert (response['message'] == 'user_logged')
    print('ok login')


if __name__ == '__main__':
    test_reset_db()
    test_auto_sign_up()
    test_login_password_incorrect()
    test_login_correctly()
