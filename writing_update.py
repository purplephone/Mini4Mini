import jwt
import time
from pymongo import MongoClient
import certifi
from flask import Flask, render_template, request, jsonify, g, Blueprint, redirect, url_for

app = Flask(__name__)

writing_update_api = Blueprint('writing_update_api', __name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.ldbjw.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta
SECRET_KEY = 'SPARTA'

@writing_update_api.route('/writing_update', methods=["GET"])
def writing_update():
    id = request.args.get("id_give")
    user = db.writing.find_one({'id':int(id)}, {'_id': False})
    return render_template('writing_update.html', user=user)


@writing_update_api.route('/update_writing', methods=["POST"])
def update_writing():
    # db 저장
    id_receive = request.form['id_give']
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    category_receive = request.form['category_give']
    print(id_receive, title_receive, content_receive, category_receive)
    db.writing.update_one({'id': int(id_receive)}, {'$set': {'title': title_receive}})
    db.writing.update_one({'id': int(id_receive)}, {'$set': {'content': content_receive}})
    db.writing.update_one({'id': int(id_receive)}, {'$set': {'category': category_receive}})
    return jsonify({'result': 'success', 'msg': '수정되었습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)