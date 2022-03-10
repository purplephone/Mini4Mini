import jwt
from flask import Flask, render_template, jsonify, g, Blueprint, request, redirect, url_for
from config import SECRET_KEY, DB_LINK, CA

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
mainPage = Blueprint('mainPage_api', __name__)

@mainPage.route('/', methods=["GET"])
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        # 로그인 복호화
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        return render_template('mainPage.html', user=payload['user'])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login_api.login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login_api.login"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
