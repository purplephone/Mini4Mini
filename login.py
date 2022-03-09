import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask import Blueprint


login_api = Blueprint('login_api',__name__)
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.zv3yk.mongodb.net/cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

@login_api.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@login_api.route('/user/<username>')
def user(username):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@login_api.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash},{"_id":False})
    print(result)
    if result is not None:
        payload = {
         'user': result,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@login_api.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    phonenum_receive = request.form['phonenum_give']
    email_receive = request.form['email_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,
        "password": password_hash,
        "nickname": nickname_receive,
        "phone_num": phonenum_receive,
        "email" : email_receive
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@login_api.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@login_api.route('/sign_up/check_nickname', methods=['POST'])
def check_nickname():
    nickname_receive = request.form['nickname_give']
    exists = bool(db.users.find_one({"username": nickname_receive}))
    return jsonify({'result': 'success', 'exists': exists})