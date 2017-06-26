#!/usr/bin/env python

from flask import Flask, render_template, request, jsonify, redirect, make_response, session, url_for
from werkzeug.utils import secure_filename
from collections import Counter
from jinja2 import Template
# from util import Util
from bson.son import SON
from pymongo import MongoClient, GEO2D


app = Flask(__name__)
#
# u = Util()
# db = u.dbConfig()
app.secret_key = 'akshdjasdGHJsslkgajh'
db = MongoClient('52.15.58.213', 27017).test


@app.route('/')
def dashboardRouting():
    if not session.get('logged_in'):
        session.clear()
        return render_template('login.html')

    elif session['logged_in'] == True:
        return home()


@app.route('/home')
def home():
    query = db.data.find({})

    # queryTwo = db.test1.find({})
    uniqueStudios = db.data.find({}).distinct("Studio")

    # for u in uniqueStudios:
    #
    # data = db.data.aggregate([
    #     {"$match": {'studio': "14th"}},
    #     {"$group": {
    #         "_id": "studio", "total": {
    #                          "$sum": "UniqueClients"
    #         }
    #     }
    #     }
    # ])
    #
    # for d in data:
    #     print d

    return render_template('index.html', query=query)


@app.route('/login', methods=['POST', 'GET'])
def do_admin_login():
    form_username = str(request.form['username']).lower()
    form_password = str(request.form['password'])

    credential = db.profiles.find_one({'username': form_username})
    if credential != None:

        db_username = str(credential['username']).lower()
        db_password = str(credential['password'])

        if form_username == db_username and form_password == db_password:
            session['logged_in'] = True
            session['studio'] = credential['studio']
            return redirect("/", code=302)
        else:
            return 'password'
    else:
        return 'username'


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
