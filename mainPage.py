import jwt
from flask import Flask, render_template, jsonify, g, Blueprint, request, redirect, url_for
from config import SECRET_KEY, DB_LINK, CA

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
mainPage = Blueprint('mainPage_api', __name__)


# mainPage 렌더링 요청
@mainPage.route('/', methods=["GET"])
def home():
    # 로그인 중인 사용자의 토큰 값 받아오기
    token_receive = request.cookies.get('mytoken')
    try:
        # 토큰 값 복호화
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # Jinja2를 이용하여 사용자 정보를 담아서 렌더링
        return render_template('mainPage.html', user=payload['user'])
    # 예외 처리
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_api.login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_api.login"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
