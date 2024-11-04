import pytest
import os

from blog_app import create_app


@pytest.fixture()
def app():
    app = create_app(Testing=True)
    
    # set up code
    with app.app_context():
        from blog_app.db import database
        database.init_app(app)
        print(app.config)
    
    yield app
    # clean up 
    

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()