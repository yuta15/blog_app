"""
DBのモデルを定義するファイル。
必要に応じて適宜モデルを作成する。
なお、定義の際、MySQLを使用しているため、Str型のカラムはlengthの指定が必須となる。
"""
import bcrypt
from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from blog_app.db.database import Base
from blog_app.db.database import DB_session


class User(Base):
    """
    ログイン管理用テーブル
    """
    __tablename__ = 'user_account'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(length=30), unique=True, nullable=False)
    user_password: Mapped[str] = mapped_column(String(length=100), nullable=False)
    user_email: Mapped[str] = mapped_column(String(length=100), nullable=False)
    user_created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    
    posts: Mapped[List['Post']] = relationship(back_populates='user')
    comments: Mapped[List['Comment']] = relationship(back_populates='user')
    
    
    @validates("user_name")
    def validate_username(self, key, user_name):
        """ユーザー名の検証"""
        if user_name is None:
            raise ValueError('Username cannot empty')
        elif not isinstance(user_name, str):
            raise ValueError('Username must be a String')
        elif len(user_name) < 3 or len(user_name) > 30:
            raise ValueError('Username must be at least 3 and no more than 30 characters.')
        else:
            return user_name
    
    
    @validates("user_password")
    def validate_password(self, key, user_password):
        """パスワード検証。戻り値はハッシュ化"""
        if user_password is None:
            raise ValueError('Password cannot empty')
        elif not isinstance(user_password, str):
            raise ValueError('Password must be a Sting')
        elif len(user_password) < 8:
            raise ValueError('Password must be more at least 8 characters')
        else:
            hashed_password = bcrypt.hashpw(password=user_password.encode('utf-8'), salt=bcrypt.gensalt())
            return hashed_password
        
        
    @validates("user_email")
    def validate_email(self, key, user_email):
        """e-mail検証"""
        if user_email is None:
            raise ValueError('e-mail cannot empty')
        elif not isinstance(user_email, str):
            raise ValueError('e-mail must be a String')
        elif '@' not in user_email:
            raise ValueError('e-mail must be included "@"')
        else:
            return user_email
        
        
    def __repr__(self) -> str:
        return f"""
            User(
                id:{self.user_id!r},
                user_name:{self.user_name!r}, 
                user_email:{self.user_email}, 
                created_at:{self.user_created_at}, 
                updated_at:{self.user_created_at}, 
                is_admin:{self.is_admin}
            )
        """


class Post(Base):
    """
    ブログ投稿用テーブル。
    """
    __tablename__ = "post"
    post_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_title: Mapped[str] = mapped_column(String(length=150), nullable=False)
    post_content_path: Mapped[str] = mapped_column(String(length=500), nullable=False)
    post_created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    post_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    post_status: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_account.user_id'))
    
    user: Mapped[User] = relationship(back_populates="posts")
    comments: Mapped[List['Comment']] = relationship(back_populates='post')

    def __repr__(self) -> str:
        return f"""
            Post(
                id:{self.post_id!r}, 
                user_name:{self.post_title!r}, 
                user_email:{self.post_content_path!r}, 
                created_at:{self.post_created_at!r}, 
                updated_at:{self.post_updated_at!r}, 
                user_id:{self.user_id!r}
            )
        """


class Comment(Base):
    """
    コメント用テーブル。
    """
    __tablename__ = "comment"
    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_content: Mapped[str] = mapped_column(String(length=300), nullable=False)
    comment_created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.post_id'))
    post: Mapped[Post] = relationship(back_populates="comments")
    
    user_id: Mapped[User] = mapped_column(Integer, ForeignKey('user_account.user_id'))
    user: Mapped[User] = relationship(back_populates="comments")

    def __repr__(self) -> str:
        return f"""
            Comment(
                comment_id:{self.comment_id!r}
                comment_content:{self.comment_content!r}
                created_at:{self.comment_created_at!r}
                post_id:{self.post_id!r}
                user_id:{self.user_id!r}
            )
    """

