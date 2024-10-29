from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask import jsonify
from datetime import datetime

from blog_app.db.database import DB_session
from blog_app.db.models.models import User



auth = Blueprint("auth", __name__, url_prefix='/auth')


@auth.route('/register', methods=('POST'))
def register():
    """
    新規ユーザ登録用関数。dbへ受信したデータをinsertし、結果を応答する。
    失敗した場合はロールバック処理を実施する。
    """
    db_session = DB_session()
    now = datetime.now()
    try:
        new_user = User(
            user_name = request.form['username'],
            user_password = request.form['password'],
            user_email = request.form['email'],
            user_created_at = now,
            user_updated_at = now,
            is_admin = request.form['is_admin']
        )
        db_session.add(new_user)
        db_session.commit()
        DB_session.remove()
        return jsonify({'message': 'New user created successfully'}), 200
    except:
        session.rollback()
        return jsonify({'message': 'New user created failed. Please Check your input data'}), 400
        
        