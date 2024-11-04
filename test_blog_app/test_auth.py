import pytest


def test_auth_register_return_200(client):
    """
    return code 200
    """
    data = {
        "username": "adminuser",
        "password": "adminuser",
        "email": "adminuser@gmail.com",
        "is_admin": True
    }
    data2 = {
        "username": "adminuser",
        "password": "adminuser",
        "email": "adminuser@gmail.com",
        "is_admin": False
    }
    data3 = {
        "username": "adminuser",
        "password": "adminuser",
        "email": "adminuser@gmail.com",
    }
    url = "/auth/register"
    admin_user = client.post(url, data=data)
    test_user = client.post(url, data=data2)
    no_admin = client.post(url, data=data3)
    
    assert admin_user.status_code == 200
    assert test_user.status_code == 200
    assert no_admin.status_code == 200
    