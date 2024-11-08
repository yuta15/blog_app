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
from werkzeug.exceptions import UnsupportedMediaType 
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.exc import OperationalError, DatabaseError, IntegrityError
import json
from json import JSONDecodeError

from blog_app.db.database import DB_session
from blog_app.db.models.models import User


auth = Blueprint("auth", __name__, url_prefix='/auth')


def get_user(username: str):
    """
    ユーザー情報を取得する関数
    """
    with DB_session() as db_session:
        try:
            if isinstance(username, str):
                raise TypeError('Typeerropr:type invalid')
            user = db_session.scalar(select(User).where(User.user_name == username))
            if user is None:
                raise ValueError('ValueError: not user')
        except OperationalError as e:
            db_session.rollback()
            raise e
        except DatabaseError as e:
            db_session.rollback()
            raise e
        except Exception as e:
            db_session.rollback()
            raise e
        else:
            return user


@auth.route('/register', methods=('POST',))
def register():
    """
    
    新規ユーザ登録用関数。dbへ受信したデータをinsertし、結果を応答する。
    失敗した場合はロールバック処理を実施する。
    """
    try:
        data = json.loads(request.get_json())
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        is_admin = bool(data.get('is_admin'))

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_user = User(
            user_name = username,
            user_password = password,
            user_email = email,
            user_created_at = now,
            user_updated_at = now,
            is_admin = is_admin
        )
        
        with DB_session() as db_session:
            db_session.add(new_user)
            db_session.commit()
            
    except UnsupportedMediaType:
        return jsonify({'message': 'Error: BadRequest. Please input json'}), 415
    except JSONDecodeError:
        return jsonify({'message: Error: JSONDecodeError. Please check json format'}), 400
    except ValueError:
        return jsonify({"message": "Error: ValueError. Please Check your input data"}), 400
    except TypeError:
        return jsonify({"message": "Error: TypeError. Please Check your input data"}), 400
    except IntegrityError:
        db_session.rollback()
        return jsonify({'message': 'Error: IntegrityError. Already exist user'}), 409
    except OperationalError:
        db_session.rollback()
        return jsonify({'message': 'Error: OperationalError.Database connection failed'}), 500
    except DatabaseError:
        db_session.rollback()
        return jsonify({'message': 'Error: DatabaseError. Database operation failed'}), 500
    except Exception as e:
        return jsonify({'message': f'Error: {str:e}'}), 502
    else:
        return jsonify({'message': 'Success:New user created successfully'}), 200


@auth.route('/login', methods=('POST',))
def login():
    """
    login用関数。入力データとDB内のデータを照合を行う。
    """
    try:
        data = json.loads(request.get_json())
        username = data.get('username')
        password = data.get('password')
        user = get_user(username=username)
        is_auth_result = bcrypt.checkpw(password=password.encode('utf-8'), hashed_password=user.user_password.encode('utf-8'))
        
    except UnsupportedMediaType:
        return jsonify({'message': 'Error: BadRequest. Please input json'}), 415
    except JSONDecodeError:
        return jsonify({'message': 'Error: JSONDecodeError. Please check json format'}), 400
    except TypeError:
        return jsonify({'message': 'Error: TypeError. Please check your input Data'}), 400
    except ValueError:
        return jsonify({'message': 'Error: ValueError. Please check your input Data'}), 400
    except OperationalError:
        return jsonify({'message': 'Error: OperationalError.Database connection failed'}), 500
    except DatabaseError:
        return jsonify({'message': 'Error: DatabaseError. Database operation failed'}), 500
    except Exception as e:
        return jsonify({'message': f'Error: {str:e}'}), 502
    else:
        if is_auth_result:
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