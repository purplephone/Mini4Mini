import time
from pymongo import MongoClient
import certifi
from flask import Flask, render_template, request, jsonify, g, Blueprint

app = Flask(__name__)

writing_api = Blueprint('writing_api', __name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.ldbjw.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@writing_api.route('/write')
def writing():
    writing_list = list(db.writing.find({}, {'_id': False}))
    return render_template('writing.html', writing_list=writing_list)

def getGCount():
    if not hasattr(g, 'count'):
        g.count = 0
        writing_list = list(db.writing.find({}, {'_id': False}))
        for i in writing_list:
            g.count = g.count if g.count > i['id'] else i['id']
    return g.count

@writing_api.route("/writing", methods=["POST"])
def writing_post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    category_receive = request.form['category_give']

    g.count = getGCount()
    g.count += 1
    doc = {
        'id': getattr(g, "count", 0),
        'title': title_receive,
        'content': content_receive,
        'category': category_receive,
        'date': time.strftime('%m-%d %H:%M'),
        'nickname': 'nickname'
    }
    db.writing.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '등록되었습니다.'})

@writing_api.route("/writing", methods=["GET"])
def writing_get():
    writing_list = list(db.writing.find({}, {'_id': False}))
    return jsonify({'writing':writing_list})

@writing_api.route("/writing/delete", methods=["POST"])
def writing_delete():
    id_receive = request.form['id_give']
    db.writing.delete_one({'id': int(id_receive)})
    return jsonify({'result': 'success', 'msg': '삭제되었습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)