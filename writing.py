import jwt
import time
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, g, Blueprint, redirect, url_for
import os
from config import SECRET_KEY, DB_LINK, CA

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
writing_api = Blueprint('writing_api', __name__)

client = MongoClient(DB_LINK, tlsCAFile=CA)
db = client.dbsparta

# 글쓰기 페이지 렌더링 전에 로그인 여부 확인
@writing_api.route('/writing')
def writing():
    writing_list = list(db.writing.find({}, {'_id': False}))
    token_receive = request.cookies.get('mytoken')
    try:
        # 로그인 복호화
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        return render_template('writing.html', writing_list=writing_list)
    # 로그인을 안 했거나 기간 만료 시 로그인 페이지로 이동
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_api.login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_api.login"))

# 게시글 개수 카운트하는 전역변수
def getGCount():
    if not hasattr(g, 'count'):
        count_one = db.count.find_one({"name": "count"}, {'_id': False})
        print(count_one)
        if count_one:
            g.count = count_one["val"]
        else:
            doc = {
                "name": "count",
                "val": 100
            }
            db.count.insert_one(doc)
            g.count = 100
    return g.count

# 게시글 db저장 후 글 카운트 증가 후 번호 부여
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
    db.count.update_one({"name":"count"}, {'$set': {'val': g.count}})
    return jsonify({'result': 'success', 'msg': '등록되었습니다.', 'writing_id': getattr(g, "count", 0)})

# db에 저장되어 있는 게시글 가져오기
@writing_api.route("/writing/get", methods=["GET"])
def writing_get():
    # db 가져오기
    search = request.args.get("search")
    sort = request.args.get("sort")

    writing_list = list(db.writing.find({}, {'_id': False}))
    # 좋아요(즐겨찾기) 필터 기능
    if search:
        if search == "like":
            user_id = request.args.get("user_id")
            like_list = list(db.like.find({"user_id": user_id}, {'_id': False}))
            like_id_list = [int(x['writing_id']) for x in like_list]
            writing_list = list(db.writing.find({"id": {"$in": like_id_list}}, {'_id': False}))
        else:
            writing_list = list(db.writing.find({"category": search}, {'_id': False}))

    # 게시글 최신 순, 오래된 순, 추천 순으로 정렬
    if sort == "old":
        writing_list.sort(key=lambda x: x["id"])
    elif sort == "like":
        writing_list.sort(key=lambda x: -x["like_count"])
    else:
        writing_list.sort(key=lambda x: -x["id"])

    return jsonify({'writing': writing_list})

# 게시글 클릭했을 때 모달 폼으로 보여주기 위한 정보 가져오기
@writing_api.route("/writing/get/<id>", methods=["GET"])
def writing_get_one(id):
    writingOne = db.writing.find_one({'id': int(id)}, {'_id': False})
    return jsonify({'writing': writingOne})

# 게시글 및 사진 삭제
@writing_api.route("/writing/delete", methods=["POST"])
def writing_delete():
    id_receive = request.form['id_give']
    user = db.writing.find_one({'id':int(id_receive)})
    if(user['file'] != ""):
        os.remove('static/' + user['file'])
    db.writing.delete_one({'id': int(id_receive)})
    return redirect("/")


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)