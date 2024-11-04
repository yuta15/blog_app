"""
FlaskのFactoryファイル。
テスト時もこのcreate_app()を呼び出すことでアプリケーションを実行する。
各種機能はBlueprintにて分割するため、新規機能追加時には本ファイルへ記述する。
テスト時には、create_app(Testing=True)とすることでapp.config内の設定がテスト用の設定となる。
"""

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