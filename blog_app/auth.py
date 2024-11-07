"""
認証機能用ファイル。
ログイン、ログアウト、セッション管理機能は本ファイルに記述する。
"""


import bcrypt
from datetime import datetime
from flask import Blueprint
from flask import request
from flask import session
from flask import jsonify
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError

from blog_app.db.database import DB_session
from blog_app.db.models.models import User


auth = Blueprint("auth", __name__, url_prefix='/auth')


# APIにて使用する関数
def get_user(username: str):
    """
    ユーザー情報を取得する関数
    """
    with DB_session() as db_session:
        try:
            user = db_session.scalar(select(User).where(User.user_name == username))
        except DBAPIError as e:
            raise e
        else:
            return user


def check_exist_user(username: str):
    """
    ユーザー情報を取得するための関数
    args:
        username: str
            ユーザー名
    return:
        ユーザーが存在する場合、Trueを返す。
    """
    try:
        user = get_user(username=username)
    except DBAPIError as e:
        raise e
    else:
        if user is None:
            return False
        else:
            return True
    

def user_authentication(username, password: str):
    """
    ユーザー認証用関数
    args:
        username: str
            ユーザー名
        password: str
            パスワード
    return:
        認証が成功した場合Trueを返す。
    """
    try:
        user = get_user(username=username)
    except DBAPIError:
        raise
    else:
        if user is not None:
            check_password = bcrypt.checkpw(
                password=password.encode('utf-8'), 
                hashed_password=user.user_password.encode('utf-8')
                )
            return check_password


# 以下API用関数
@auth.route('/register', methods=('POST',))
def register():
    """
    
    新規ユーザ登録用関数。dbへ受信したデータをinsertし、結果を応答する。
    失敗した場合はロールバック処理を実施する。
    """
    try:
        username = request.form.get(key='username')
        password = request.form.get(key='password')
        email = request.form.get(key='email')
        is_admin = bool(request.form.get(key='is_admin', default=False))
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_user = User(
            user_name = username,
            user_password = password,
            user_email = email,
            user_created_at = now,
            user_updated_at = now,
            is_admin = is_admin
        )
        
        if check_exist_user(username):
            # ユーザ名が既に存在する場合に実行
            return jsonify({"message": "User is exists"}), 409
        
        with DB_session() as db_session:
            db_session.add(new_user)
            db_session.commit()
            
    except ValueError:
        # 入力した値に不備があった場合にキャッチ
        return jsonify({"message": "Failed:New user created failed. Please Check your input data"}), 400
            
    except DBAPIError as e:
        # DBエラーが発生した場合にキャッチ
        db_session.rollback()
        return jsonify({'message': 'Error: server error'}), 500
    
    else:
        return jsonify({'message': 'Success:New user created successfully'}), 200



@auth.route('/login', methods=('POST',))
def login():
    """
    login用関数。入力データとDB内のデータを照合を行う。
    """
    try:
        username = request.form.get(key='username')
        password = request.form.get(key='password')
        user = get_user(username=username)
        user_auth_result = user_authentication(username=username, password=password)
    except DBAPIError:
        return jsonify({'message': 'Error: server error'}), 500
    else:
        if user_auth_result:
            session['username'] = user.user_name
            session['is_authenticated'] = True
            session['is_admin'] = user.is_admin
            return jsonify({'message': 'Success: login successfully'}), 200
        else:
            return jsonify({'message': 'Failed: login failed'}), 401
    
    
@auth.route('/logout', methods=('GET',))
def logout():
    """
    logout用関数。セッションを外す。
    """
    session.clear()
    return jsonify({"message": "Successfully: logout success"}), 200


@auth.route('/check_session', methods=('GET',))
def check_session():
    """
    session情報をチェックする関数
    """
    if session.get('is_authenticated'):
        return jsonify({"message": "login"}), 200
    else:
        return jsonify({"message": "not session"}), 401