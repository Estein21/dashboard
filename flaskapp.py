from flask import Flask, render_template, request, jsonify, redirect, make_response, session, url_for
from pymongo import MongoClient, GEO2D
from werkzeug.utils import secure_filename
from collections import Counter
from jinja2 import Template
from util import Util

app = Flask(__name__)

u = Util()
db = u.dbConfig()

@app.route('/')
def home():
    query = db.test1.find({})
    return render_template('index.html', query = query)

@app.route('/upload')
def upload_page():
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
