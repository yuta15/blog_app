"""
DB操作に関する部分を記述するファイル。
engin定義、sessionの定義等はこのファイルで実行する為、各種機能はこのファイルをインポートし、
DBの操作を実行する。
なお、flaskコマンドにて使用する初期化用のコマンド定義についてもこのファイルで定義し、Factoryで読み込むことで使用する。
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from flask import current_app
from flask import g

import click

engin = None
DB_session = None


class Base(DeclarativeBase):
    """Baseモデルの定義"""
    pass


def init_engin(database_uri):
    """
    enginの初期化
    """
    global engin, DB_session
    engin = create_engine(database_uri)
    DB_session = sessionmaker(bind=engin)


def create_table():
    """
    新規テーブル作成用関数
    """
    from blog_app.db.models.models import User
    from blog_app.db.models.models import Post
    from blog_app.db.models.models import Comment
    
    Base.metadata.create_all(bind=engin)
    click.echo('\nInitialized db')


def drop_table():
    """
    既存のテーブルを削除する関数
    ※テーブルが削除され、テーブル内の情報をすべて失います。
    ※使用には要注意
    """
    from blog_app.db.models.models import User
    from blog_app.db.models.models import Post
    from blog_app.db.models.models import Comment
    
    Base.metadata.drop_all(bind=engin)
    click.echo('\nDropped all tables')


def init_app(app):
    """DB初期化用関数.Flaskコマンドから実行可能"""
    
    init_engin(app.config['DATABASE_URI'])
    
    @app.cli.command('init-db')
    def init_db_command():
        create_table()
        
    @app.cli.command('drop-table')
    def drop_table_command():
        drop_table()

