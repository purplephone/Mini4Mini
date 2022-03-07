from flask import Flask, render_template, request, jsonify, g
app = Flask(__name__)

from pymongo import MongoClient
import certifi


ca = certifi.where()
client = MongoClient('mongodb+srv://root:root@cluster0.0wmzg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta



@app.route('/')
def home():

    search = request.args.get('search')
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

    return render_template('main_Login.html', writing_list=writing_list, id="test1")



@app.route("/loadMain", methods=["GET"])
def loadMain():
    count = len(list(db.writing.find({}, {'_id': False})))
    count += 1
    title = "this is title" + str(count)
    content = "this is test contents" + str(count)
    doc = {
        "id": count,
        "title": title,
        "content": content,
        "category": "javascript",
        "nickname": "test"
    }

    db.writing.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)