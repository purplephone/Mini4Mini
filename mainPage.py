import jwt
from flask import Flask, render_template, jsonify, g, Blueprint, request, redirect, url_for

app = Flask(__name__)
mainPage = Blueprint('mainPage_api', __name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
# client = MongoClient('mongodb+srv://test:sparta@cluster0.hdgtj.mongodb.net/Cluster0?retryWrites=true&w=majority',
#                      tlsCAFile=ca)
# 테스트용
client = MongoClient('mongodb+srv://root:root@cluster0.0wmzg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

SECRET_KEY = 'SPARTA'


@mainPage.route('/', methods=["GET"])
def home():
    token_receive = request.cookies.get('mytoken')
    search = request.args.get('search')
    try:
        writing_list = list(db.writing.find({}, {'_id': False}))
        # 필터 기능
        if search:
            if search == "html":
                writing_list = list(db.writing.find({"category": "html"}, {'_id': False}))
            elif search == "javascript":
                writing_list = list(db.writing.find({"category": "javascript"}, {'_id': False}))
            elif search == "flask":
                writing_list = list(db.writing.find({"category": "flask"}, {'_id': False}))
            elif search == "mongodb":
                writing_list = list(db.writing.find({"category": "mongodb"}, {'_id': False}))

        # 로그인 복호화
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('mainPage.html', user=payload, writing_list=writing_list)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_api.login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_api.login"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
