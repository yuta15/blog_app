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


@pytest.fixture(scope='module')
def create_user():
    def _create_user(username, password, email):
        from blog_app.db import database
        from blog_app.db.models.models import User
        from datetime import datetime

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        setup_user = User(
            user_name = username,
            user_password = password,
            user_email = email,
            user_created_at = now,
            user_updated_at = now,
        )
        with database.DB_session() as db_session:
            db_session.add(setup_user)
            db_session.commit()
            
    return _create_user