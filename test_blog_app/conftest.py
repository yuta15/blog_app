import pytest

from blog_app import create_app
from blog_app.db import database



@pytest.fixture()
def app():
    app = create_app()
    app.config.from_pyfile('test_config.py', silent=False)
    
    # set up code
    with app.app_context():
        database.init_app(app=app)
    
    yield app
    # clean up 
    

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()