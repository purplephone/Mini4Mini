import jwt
import time
from pymongo import MongoClient
import certifi
from flask import Flask, render_template, request, jsonify, g, Blueprint, redirect, url_for
import os

app = Flask(__name__)

writing_api = Blueprint('writing_api', __name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.hdgtj.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

SECRET_KEY = 'SPARTA'


@writing_api.route('/writing')
def writing():
    writing_list = list(db.writing.find({}, {'_id': False}))
    token_receive = request.cookies.get('mytoken')
    try:
        # 로그인 복호화
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        return render_template('writing.html', writing_list=writing_list)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_api.login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_api.login"))


def getGCount():
    if not hasattr(g, 'count'):
        g.count = 0
        writing_list = list(db.writing.find({}, {'_id': False}))
        for i in writing_list:
            g.count = g.count if g.count > i['id'] else i['id']
    return g.count


@writing_api.route("/writing", methods=["POST"])
def writing_post():
    # db 저장
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    category_receive = request.form['category_give']

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    print(payload)

    g.count = getGCount()
    g.count += 1
    doc = {
        'id': getattr(g, "count", 0),
        'title': title_receive,
        'content': content_receive,
        'category': category_receive,
        'date': time.strftime('%m-%d %H:%M'),
        'nickname': payload['user']['nickname'],
        'like_count': 0,
        'file': ""
    }
    db.writing.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '등록되었습니다.', 'writing_id': getattr(g, "count", 0)})


@writing_api.route("/writing/get", methods=["GET"])
def writing_get():
    # db 가져오기
    search = request.args.get("search")
    writing_list = list(db.writing.find({}, {'_id': False}).sort("id", -1))
    print(writing_list)
    # 필터 기능
    if search:
        if search == "like":
            user_id = request.args.get("user_id")
            like_list = list(db.like.find({"user_id": user_id}, {'_id': False}))
            like_id_list = [int(x['writing_id']) for x in like_list]
            writing_list = list(db.writing.find({"id": {"$in": like_id_list}}, {'_id': False}))
        else:
            writing_list = list(db.writing.find({"category": search}, {'_id': False}))

    return jsonify({'writing':writing_list})


@writing_api.route("/writing/get/<id>", methods=["GET"])
def writing_get_one(id):
    writingOne = db.writing.find_one({'id': int(id)}, {'_id': False})
    return jsonify({'writing': writingOne})


@writing_api.route("/writing/delete", methods=["POST"])
def writing_delete():
    id_receive = request.form['id_give']
    user = db.writing.find_one({'id': int(id_receive)}, {'_id': False})
    os.remove('static/' + user['file'])
    db.writing.delete_one({'id': int(id_receive)})
    return redirect("/")


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)