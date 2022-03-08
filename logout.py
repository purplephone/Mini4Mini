import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask import Blueprint

login_api = Blueprint('login_api',__name__)
from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.hdgtj.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta



@app.route('/logout', methods=['GET']) # POST는 필요없다.
def logout():
	    session.pop('userid', None)
    return redirect('/')