import os
from flask import Flask


def create_app(Testing:bool=False):
    """
    アプリケーションの作成と設定用関数
    """
    if Testing:
        # test実行時は環境変数を変更する。
        os.environ['FLASK_ENV'] = 'Test'
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
        
    # 新規テーブルの作成
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