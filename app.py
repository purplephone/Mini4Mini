from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

from login import login_api

app.register_blueprint(login_api)

# 임재현 수정
from mainPage import mainPage

app.register_blueprint(mainPage)

# 김경래 수정
from writing import writing_api

app.register_blueprint(writing_api)

from writing_update import writing_update_api

app.register_blueprint(writing_update_api)

# 임재현 수정
from like import like_api

app.register_blueprint(like_api)

from upload import upload_api

app.register_blueprint(upload_api)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)