from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import Blueprint
from pymongo import MongoClient
from config import SECRET_KEY, DB_LINK, CA

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
upload_api = Blueprint('upload_api',__name__)

client = MongoClient(DB_LINK, tlsCAFile=CA)
db = client.dbsparta


@upload_api.route('/upload')
def load_file():
    return render_template('upload.html')


@upload_api.route('/upload/<id>', methods=['POST'])
def upload_file(id):
    if request.method == 'POST':
        f = request.files['file']
        if(f.filename == ''):
            return jsonify({'result': 'success', 'msg': '파일 업로드 성공.'})

        print(f)
        extension = f.filename.split(".")[-1]
        f.filename = str(id) + "." + extension
        f.save("./static/"+secure_filename(f.filename))
        print(f.filename)
        db.writing.update_one({'id': int(id)}, {'$set': {'file': f.filename}});
        return jsonify({'result': 'success', 'msg': '파일 업로드 성공.'})



if __name__ == '__main__':
    app.run(debug=True)