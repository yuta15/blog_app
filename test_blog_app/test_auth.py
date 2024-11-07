import pytest


def test_auth_register_return_200(client):
    """
    url: auth/register
    status_code: 200
    """
    data1 = {
        "username": "user1",
        "password": "adminuser",
        "email": "adminuser@gmail.com",
        "is_admin": True
    }
    data2 = {
        "username": "user2",
        "password": "adminuser",
        "email": "adminuser@gmail.com",
        "is_admin": False
    }
    data3 = {
        "username": "user3",
        "password": "adminuser",
        "email": "adminuser@gmail.com",
    }
    url = "/auth/register"
    user1 = client.post(url, data=data1)
    user2 = client.post(url, data=data2)
    user3 = client.post(url, data=data3)
    
    assert user1.status_code == 200
    assert user2.status_code == 200
    assert user3.status_code == 200
    
    
def test_auth_register_return_400(client):
    """
    url: auth/register
    status_code: 400
    """
    username_test = [
        {"username": None, "password": "adminuser", "email": "adminuser@gmail.com"},
        {"username": "12", "password": "adminuser", "email": "adminuser@gmail.com"},
        {"username": "1111111111111111111111111111111", "password": "adminuser", "email": "adminuser@gmail.com"},
    ]
    password_test = [
        {"username": "400_user1", "password": None, "email": "adminuser@gmail.com"},
        {"username": "400_user2", "password": "passwor", "email": "adminuser@gmail.com"},
        {"username": "400_user3", "password": "1234567", "email": "adminuser@gmail.com"},
    ]
    email_test = [
        {"username": "400_user4", "password": "password", "email": None},
        {"username": "400_user5", "password": "password", "email": 1234},
        {"username": "400_user6", "password": "password", "email": "adminusergmail.com"},
    ]
    url = "/auth/register"
    
    for username, password, email in zip(username_test, password_test, email_test):
        usernmae_result = client.post(url, data=username)
        password_result = client.post(url, data=password)
        email_result = client.post(url, data=email)

        
        assert usernmae_result.status_code == 400
        assert password_result.status_code == 400
        assert email_result.status_code == 400
    
    
def test_auth_register_return_409(client):
    """
    url: auth/register
    status_code: 409
    """
    data = {
        "username": "user1",
        "password": "adminuser",
        "email": "adminuser@gmail.com",
        "is_admin": True
    }
    data2 = {
        "username": "user1",
        "password": "adminuser",
        "email": "adminuser@gmail.com",
        "is_admin": False
    }
    data3 = {
        "username": "user1",
        "password": "adminuser",
        "email": "adminuser@gmail.com",
    }
    url = "/auth/register"
    admin_user = client.post(url, data=data)
    user1 = client.post(url, data=data2)
    user2 = client.post(url, data=data3)
    
    assert admin_user.status_code == 409
    assert user1.status_code == 409
    assert user2.status_code == 409
    
    

    
