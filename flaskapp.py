from flask import Flask, render_template, request, jsonify, redirect, make_response, session
from pymongo import MongoClient, GEO2D
from collections import Counter
from jinja2 import Template
import json

app = Flask(__name__)

db = MongoClient('13.58.90.190', 27017).test

@app.route('/')
def home():
    query = db.test1.find()
    return render_template('index.html', query=query)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    return redirect("/", code=302)

@app.route('/pi')
def pi():
    return render_template('pi.html')

if __name__ == '__main__':
    app.run(debug=True)
