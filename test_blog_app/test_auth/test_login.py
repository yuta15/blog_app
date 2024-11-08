import pytest
import json


with open('./test_blog_app/test_auth/test_data.json') as f:
    test_data = json.load(f)
    

def test_auth_login_return_200(client, create_user):
    """
    url: auth/login
    status_code: 200
    """
    data = test_data['test_auth_login_return_200']
    create_user_val = data[0]
    test_user_val = data[1]
    create_user(create_user_val.get('username'), create_user_val.get('password'), create_user_val.get('email'))
    url = '/auth/login'
    result = client.post(url, json=json.dumps(test_user_val))
    assert result.status_code == 200
    
    
def test_auth_login_return_400(client, create_user):
    """
    status_code: 400
    """
    data = test_data['test_auth_login_return_400']
    
    