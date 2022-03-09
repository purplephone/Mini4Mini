from encodings import undefined

import jwt
import time
from pymongo import MongoClient
import certifi
from flask import Flask, render_template, request, jsonify, g, Blueprint, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

writing_update_api = Blueprint('writing_update_api', __name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.hdgtj.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
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

@writing_update_api.route('/update_img/<id>', methods=['POST'])
def update_img(id):
    if request.method == 'POST':
        writing = db.writing.find_one({'id': int(id)}, {'_id': False})
        f = request.files['file']
        if(f.filename == ''):
            return jsonify({'result': 'success', 'msg': '파일 업로드 성공.'})
        else:
            extension = f.filename.split(".")[-1]
            f.filename = str(id) + "." + extension
            if(writing['file'] != ""):
                os.remove('./static/' + writing['file'])
            f.save("./static/"+secure_filename(f.filename))
            db.writing.update_one({'id': int(id)}, {'$set': {'file': secure_filename(f.filename)}})
        return jsonify({'result': 'success', 'msg': '파일 업로드 성공.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)