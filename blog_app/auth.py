import bcrypt
from datetime import datetime
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask import jsonify
from sqlalchemy import select

from blog_app.db.database import DB_session
from blog_app.db.models.models import User


auth = Blueprint("auth", __name__, url_prefix='/auth')

@auth.route('/register', methods=('POST',))
def register():
    """
    新規ユーザ登録用関数。dbへ受信したデータをinsertし、結果を応答する。
    失敗した場合はロールバック処理を実施する。
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_user = User(
        user_name = request.form['username'],
        user_password = bcrypt.hashpw(password=request.form['password'].encode('utf-8'), salt=bcrypt.gensalt()),
        user_email = request.form['email'],
        user_created_at = now,
        user_updated_at = now,
        is_admin = False if 'is_admin' not in request.form else True
    )
    with DB_session() as db_session:
        try:
            db_session.add(new_user)
            db_session.commit()
            return jsonify({'message': 'New user created successfully'}), 200
        except Exception as e:
            db_session.rollback()
            print(f"Error db access: {e}")
            return jsonify({"message": "New user created failed. Please Check your input data"}), 400



@auth.route('/get_user', methods=('GET',))
def get_uer():
    """
    DBテスト用関数。selectが正常に動作することをテスト
    """
    with DB_session() as db_session:
        try:
            stmt = select(User)
            users = db_session.execute(stmt).scalars().all()
            # print(users)
            ret_users = []
            for user in users:
                ret_users.append({
                    "user_id": user.user_id,
                    "user_name": user.user_name,
                    "user_password": user.user_email,
                    "user_email": user.user_email,
                    "user_created_at": user.user_created_at,
                    "user_updated_at": user.user_updated_at,
                    "is_admin": user.is_admin,
                })
            print(ret_users)
            return jsonify(response=ret_users), 200
        except:
            return jsonify({"message": "User datas get failed from database"})