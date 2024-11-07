import pytest
import os

from blog_app import create_app


@pytest.fixture(scope='module')
def app():
    app = create_app(Testing=True)
    
    # set up code
    with app.app_context():
        from blog_app.db import database
        database.init_engin(app.config['DATABASE_URI'])
        database.create_table()
        
    yield app
    # clean up 
    
    with app.app_context():
        database.drop_table()
    

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()