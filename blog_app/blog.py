"""
ブログ管理用機能。
ブログの投稿、保存、修正、閲覧等のブログに関する機能は本ファイルに記述する。
なお、機能拡張に伴いファイルサイズが大きくなる場合には適宜拡張予定。
"""

from datetime import datetime
from flask import Blueprint
from flask import request
from flask import session
from flask import jsonify
from flask import current_app, g
from sqlalchemy import select
from werkzeug.utils import secure_filename
import os

from blog_app.db.database import DB_session
from blog_app.db.models.models import Post, User


blog = Blueprint("blog", __name__, url_prefix='/blog')



def check_user_id(username):
    try:
        with DB_session() as db_session:
            stmt = select(User).where(username)
            user = db_session.execute(stmt).scalar().all()
            return user[0].user_id
    except Exception as e:
        raise e


def check_session():
    if session.get('is_authenticated'):
        return True
    else:
        return False


@blog.route('/new_post', methods=('POST', ))
def new_post():
    """
    新しいブログをポストするための関数。
    公開の場合、ブログ公開状態、未公開の場合はユーザーのみ閲覧可能な状態となる。
    """
    if check_session():
        title = request.form.get('title')
        username = session.get('username')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post_status = request.form.get(key='status')
        post_file = request.files.get('file')
        
        if not post_file or post_file.filename == '':
            return jsonify({"message": "file is bad files"}) , 400
        
        
        with DB_session() as db_session:
            try:
                post_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], username, secure_filename(post_file.filename))
                post_file.save(post_file_path)
                new_post = Post(
                    post_title = title,
                    post_content = post_file_path,
                    post_created_at = now,
                    post_updated_at = now,
                    post_status = post_status,
                    user_id = check_user_id(username)
                )
                db_session.add(new_post)
                db_session.commit()
                return ({"message": "Success: new file saved successfully"}), 200
            except Exception as e:
                db_session.rollback()
                return ({"message": "Failed: new file save failed"}), 500
        
    else:
        return jsonify({"message": "Fialed: please login "}), 401


# @blog.route('list', methods=('GET',))
# def list_posts():
    