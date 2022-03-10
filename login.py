import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask import Blueprint
from pymongo import MongoClient
from config import SECRET_KEY, DB_LINK, CA

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
login_api = Blueprint('login_api',__name__)

client = MongoClient(DB_LINK, tlsCAFile=CA)
db = client.dbsparta

@login_api.route('/login')
def login():
    # 로그인 화면을 렌더링
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@login_api.route('/sign_in', methods=['POST'])
def sign_in():
    # 클라이언트로부터 username, password를 받아옴
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    # 보안상의 이유로 비밀번호를 SHA256으로 해쉬 후 저장
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash},{"_id":False})
    if result is not None:
        # 토큰의 유효기간을 24시간으로 설정
        payload = {
         'user': result,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        # JWT 토큰 생성
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # 토큰을 클라이언트에 전달
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@login_api.route('/sign_up/save', methods=['POST'])
def sign_up():
    # 회원가입 정보를 클라이언트로부터 받아옴
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    phonenum_receive = request.form['phonenum_give']
    email_receive = request.form['email_give']
    # 비밀번호는 SHA256으로 해쉬 후 저장
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # 회원정보 입력
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
    # 데이터베이스에 같은 username이 존재하는지 확인
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@login_api.route('/sign_up/check_nickname', methods=['POST'])
def check_nickname():
    # 데이터베이스에 같은 nickname이 존재하는지 확인
    nickname_receive = request.form['nickname_give']
    exists = bool(db.users.find_one({"username": nickname_receive}))
    return jsonify({'result': 'success', 'exists': exists})