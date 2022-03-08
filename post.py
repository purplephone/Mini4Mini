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
client = MongoClient('mongodb+srv://test:sparta@cluster0.hdgtj.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'
# 게시물 포스팅
@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

#전체 게시물 가져오기
@app.route("/get_posts", methods=['GET'])
def get_posts():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅 목록 받아오기
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다."})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
