import jwt
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask import Blueprint
from pymongo import MongoClient
from config import SECRET_KEY, DB_LINK, CA

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
like_api = Blueprint('like_api', __name__)

client = MongoClient(DB_LINK, tlsCAFile=CA)
db = client.dbsparta


# 로그인 중인 사용자가 누른 좋아요 목록 요청-전달
@like_api.route('/like')
def like_get_all():
    # 로그인 중인 사용자의 토큰 값 받아오기
    token_receive = request.cookies.get('mytoken')
    try:
        # 토큰 값 복호화
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 토큰 값에서 받아온 사용자 정보로 사용자가 MONGODB에서 좋아요 누른 값 find
        like_list = list(db.like.find({"user_id": payload['user']["username"]}, {'_id': False}))
        # 목록 json 반환
        return jsonify({'like_list': like_list})

    # 예외 처리
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_api.login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_api.login"))


# 특정 글에 좋아요 누른 사용자 목록 요청-전달
@like_api.route('/like/<writing_id>')
def like_get_writing(writing_id):
    # 특정 글을 좋아요 누른 사용자들의 목록 검색
    like_list = list(db.like.find({"writing_id": writing_id}, {'_id': False}))
    return jsonify({'like_list': like_list})


# 좋아요 목록 추가
@like_api.route('/like', methods=["POST"])
def like_post():
    doc = {
        "user_id": request.form["user_id"],
        "writing_id": request.form["writing_id"]
    }
    db.like.delete_many(doc)
    db.like.insert_one(doc)
    like_update(request.form["writing_id"])

    return jsonify({'result': 'success', 'msg': '북마크 추가되었습니다.'})


# 좋아요 목록 취소
@like_api.route('/like', methods=["DELETE"])
def like_delete():
    doc = {
        "user_id": request.form["user_id"],
        "writing_id": request.form["writing_id"]
    }
    # delete_one을 해도 똑같이 동작하지만
    # 중복 정보가 있을 경우를 고려하여 해당 정보를 가지는 객체 전부 삭제
    db.like.delete_many(doc)

    like_update(request.form["writing_id"])
    return jsonify({'result': 'success', 'msg': '북마크 취소되었습니다.'})


# 좋아요 변경(POST, DELETE)이 생긴 글의 좋아요 수 writing table 에 갱신
def like_update(id):
    like_list = list(db.like.find({"writing_id": id}, {'_id': False}))
    db.writing.update_one({'id': int(id)}, {'$set': {'like_count': len(like_list)}})
    return jsonify({'result': 'success', 'msg': '좋아요 수 갱신했습니다.'})