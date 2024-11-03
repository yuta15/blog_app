import bcrypt
from datetime import datetime
from flask import Blueprint
from flask import request
from flask import session
from flask import jsonify
from sqlalchemy import select

from blog_app.db.database import DB_session
from blog_app.db.models.models import User


auth = Blueprint("auth", __name__, url_prefix='/auth')


# APIにて使用する関数
def get_user(username: str):
    """
    ユーザー情報を取得するための関数
    """
    with DB_session() as db_session:
        try:
            stmt = select(User).where(User.user_name == username)
            user = db_session.execute(stmt).scalars().all()
            return user
        except:
            return None


def check_exist_user(user:list):
    """
    ユーザー情報がDB内に存在するか確認する関数。
    args: 
        user: [obj] 
    """
    if len(user) == 0:
        return False
    else: 
        return True
    

def user_authentication(user: list, form_password: str):
    """
    ユーザー認証用関数
    args:
        user[list]: ユーザーオブジェクトのリスト
        form_password[str]: 入力されたパスワード情報
    """
    check_user = check_exist_user(user)
    if check_user:
        check_password = bcrypt.checkpw(
            password=form_password.encode('utf-8'), 
            hashed_password=user[0].user_password.encode('utf-8')
            )
        return check_password


# 以下API用関数

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
    exist_user = get_user(request.form['username'])
    if exist_user == None:
        return jsonify({"message": "DB Error"}), 500
    elif check_exist_user(exist_user):
        return jsonify({"message": "User is exists"}), 409
    else:
        with DB_session() as db_session:
            try:
                db_session.add(new_user)
                db_session.commit()
                return jsonify({'message': 'Success:New user created successfully'}), 200
            except Exception as e:
                db_session.rollback()
                print(f"Error db access: {e}")
                return jsonify({"message": "Failed:New user created failed. Please Check your input data"}), 400


@auth.route('/login', methods=('POST',))
def login():
    """
    login用関数。入力データとDB内のデータを照合を行う。
    """
    username = request.form['username']
    password = request.form['password']
    user = get_user(username=username)
    user_auth_result = user_authentication(user = user, form_password=password)
    if user_auth_result:
        session['username'] = user[0].user_name
        session['is_authenticated'] = True
        session['is_admin'] = user[0].is_admin
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