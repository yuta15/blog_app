from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from flask import current_app
from flask import g

import click

engin = create_engine(current_app.config['DATABASE_URI'])
DB_session = sessionmaker(bind=engin, )


class Base(DeclarativeBase):
    """Baseモデルの定義"""
    pass


def create_table():
    """
    新規テーブル作成用関数
    """
    from blog_app.db.models.models import User
    from blog_app.db.models.models import Post
    from blog_app.db.models.models import Comment
    
    Base.metadata.create_all(bind=engin)
    click.echo('initialized db')


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
    click.echo('dropped all tables')


def init_app(app):
    """DB初期化用関数.Flaskコマンドから実行可能"""
    @app.cli.command('init-db')
    def init_db_command():
        create_table()
        
    @app.cli.command('drop-table')
    def drop_table_command():
        drop_table()

