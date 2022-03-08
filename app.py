import jwt
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

#mainPage.py에 편입
# SECRET_KEY = 'SPARTA'

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.hdgtj.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

# app route 삭제
# @app.route('/')
# def home():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#
#         return render_template('index.html')
#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


from login import login_api

app.register_blueprint(login_api)

# 임재현 수정
from mainPage import mainPage

app.register_blueprint(mainPage)

# 김경래 수정
from writing import writing_api

app.register_blueprint(writing_api)

from writing_update import writing_update_api

app.register_blueprint(writing_update_api)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)