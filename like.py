import jwt, json
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask import Blueprint


like_api = Blueprint('like_api',__name__)
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.hdgtj.mongodb.net/cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'


@like_api.route('/like')
def like_get_all():
    token_receive = request.cookies.get('mytoken')
    try:
        # 로그인 복호화
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        like_list = list(db.like.find({"user_id": payload['user']["username"]}, {'_id': False}))
        # like_list = list(db.like.find({},{'_id': False}))

        return jsonify({'like_list': like_list})
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_api.login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_api.login"))


@like_api.route('/like/<writing_id>')
def like_get_writing(writing_id):
    like_list = list(db.like.find({"writing_id": writing_id}, {'_id': False}))
    return jsonify({'like_list': like_list})


@like_api.route('/like', methods=["POST"])
def like_post():
    doc = {
        "user_id": request.form["user_id"],
        "writing_id": request.form["writing_id"]
    }
    db.like.delete_many(doc)
    db.like.insert_one(doc)
    like_update(request.form["writing_id"])

    return jsonify({'result': 'success', 'msg': '좋아요 추가되었습니다.'})
    # token_receive = request.cookies.get('mytoken')
    # try:
    #     # 로그인 복호화
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])



        # return jsonify({'result': 'success', 'msg': '등록되었습니다.'})

    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login_api.login"))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login_api.login"))


@like_api.route('/like', methods=["DELETE"])
def like_delete():
    doc = {
        "user_id": request.form["user_id"],
        "writing_id": request.form["writing_id"]
    }
    db.like.delete_many(doc)

    like_update(request.form["writing_id"])
    return jsonify({'result': 'success', 'msg': '좋아요 취소되었습니다.'})


def like_update(id):
    like_list = list(db.like.find({"writing_id": id}, {'_id': False}))
    db.writing.update_one({'id': int(id)}, {'$set': {'like_count': len(like_list)}})
    return 1