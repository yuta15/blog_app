from typing import List
from typing import Optional
from datetime import datetime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from blog_app.db.database import Base


class User(Base):
    """
    ログイン管理用テーブル
    """
    __tablename__ = "user_account"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(length=30), unique=True)
    user_password: Mapped[str] = mapped_column(String(length=100))
    user_email: Mapped[str] = mapped_column(String(length=100))
    user_created_at: Mapped[datetime] = mapped_column(DateTime)
    user_updated_at: Mapped[datetime] = mapped_column(DateTime)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    
    posts: Mapped[List['Post']] = relationship(back_populates='user')
    comments: Mapped[List['Comment']] = relationship(back_populates='user')

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
    post_title: Mapped[str] = mapped_column(String(length=150))
    post_content: Mapped[str] = mapped_column(String(length=10))
    post_created_at: Mapped[datetime] = mapped_column(DateTime)
    post_updated_at: Mapped[datetime] = mapped_column(DateTime)
    post_status: Mapped[bool] = mapped_column(Boolean)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_account.user_id'))
    
    user: Mapped[User] = relationship(back_populates="posts")
    comments: Mapped[List['Comment']] = relationship(back_populates='post')

    def __repr__(self) -> str:
        return f"""
            Post(
                id:{self.post_id!r}, 
                user_name:{self.post_title!r}, 
                user_email:{self.post_content!r}, 
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
    comment_content: Mapped[str] = mapped_column(String(length=300))
    comment_created_at: Mapped[datetime] = mapped_column(DateTime)
    
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

