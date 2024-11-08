import pytest
import json


with open('./test_blog_app/test_auth/test_data.json') as f:
    test_data = json.load(f)


def test_auth_register_return_200(client):
    """
    url: auth/register
    status_code: 200
    """
    datas = test_data['test_auth_register_return_200']
    url = "/auth/register"
    for data in datas:
        response = client.post(url, json=json.dumps(data))
        assert response.status_code == 200
    
    
def test_auth_register_return_400(client):
    """
    url: auth/register
    status_code: 400
    """
    datas = test_data.get('test_auth_register_return_400')
    url = "/auth/register"
    
    for data in datas:
        result1 = client.post(url, json=json.dumps(data))
        result2 = client.post(url, json=data)
        assert result1.status_code == 400
        assert result2.status_code == 400
    
    
def test_auth_register_return_409(client):
    """
    url: auth/register
    status_code: 409
    """
    datas = test_data.get('test_auth_register_return_409')
    url = "/auth/register"
    # 一回目のユーザーを追加
    client.post(url, json=json.dumps(datas))
    # 二回目のユーザーを追加
    result = client.post(url, json=json.dumps(datas))
    assert result.status_code == 409
    
    
def test_auth_register_return_415(client):
    """
    url: auth/register
    status_code: 415
    """
    data = test_data.get('test_auth_register_return_415')
    url = "/auth/register"
    result = client.post(url, data=data)
    assert result.status_code == 415
