import os
from flask import Flask


def create_app():
    """
    アプリケーションの作成と設定用関数
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(
        'config.py',
    )    
    # db init
    with app.app_context():
        from blog_app.db import database
        database.init_app(app)
    # auth function
    from . import auth
    app.register_blueprint(auth.auth)
    # blog function
    from . import blog
    app.register_blueprint(blog.blog)
    # setting function
    
    
    return app