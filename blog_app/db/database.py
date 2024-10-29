from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from flask import current_app
from flask import g

import click


engin = create_engine(current_app.config['DATABASE_URI'])
DB_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engin))


class Base(DeclarativeBase):
    """Baseモデルの定義"""
    pass




def shutdown_session():
    """セッションクリーンアップ用関数"""
    DB_session.remove()
    
    
def init_app(app):
    @app.cli.command("init-db")
    def init_db():
        from blog_app.db.models.models import User
        from blog_app.db.models.models import Post
        from blog_app.db.models.models import Comment
        
        Base.metadata.create_all(bind=engin)
        click.echo('initialized db')
