"""
このファイルは、Flaskのapp.configに設定する為のファイル。
環境変数にて設定した値はこのファイルで読み込むことでFlask内で使用可能となる。
共通設定はテスト、開発時に同時に実行しますが、必要な場合は適宜修正。
環境変数には、最低限以下設定が必要

[環境変数]
- FLASK_ENV: 環境
- FLASK_ROOT_DIR: ルートディレクトリ
- DB_USERNAME: DBのユーザー名
- DB_PASSWORD: DBのパスワード
- DB_PORT: DBのポート番号
"""

import os
import secrets
import pymysql

# 環境の設定
FLASK_ENV = os.environ.get('FLASK_ENV')
APPLICATION_ROOT  = os.environ.get('FLASK_ROOT_DIR')
FLASK_APP = os.environ.get('FLASK_APP')

# 環境差分設定
if FLASK_ENV == 'Dev':
    # Dev環境用の設定は以下へ記述
    DB_PORT = os.environ.get('DB_PORT')
    UPLOAD_FOLDER = os.path.join(APPLICATION_ROOT, "uploads")
    DB_HOSTNAME = os.environ.get('DB_HOSTNAME')
    
elif FLASK_ENV == 'Test':
    # テスト環境用の設定は以下へ記述
    TESTING = True
    DB_PORT = os.environ.get('TEST_DB_PORT')
    DB_HOSTNAME = os.environ.get('TEST_DB_HOSTNAME')
    UPLOAD_FOLDER = os.path.join(APPLICATION_ROOT, 'test_uploads')

# DB設定
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Flask
ALLOWED_EXTENSIONS = {'.md'}
DEBUG = True
FLASK_SECRET_KEY = secrets.token_hex(10)
DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/blog_app"