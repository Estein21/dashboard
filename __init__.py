#!/usr/bin/env python

from flask import Flask, render_template, request, jsonify, redirect, make_response, session, url_for
from werkzeug.utils import secure_filename
from collections import Counter
from jinja2 import Template
from bson.son import SON
from pymongo import MongoClient, GEO2D
from suds.client import Client
from bson import json_util
import json

#objects made by me
from objects.Utilities import Utilities
from objects.ClassService import ClassServiceCalls



app = Flask(__name__)

util = Utilities()
db = util.dbConfig()

app.secret_key = util.secretKey


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

    # total sessions sum
    queryTwo = db.data.find()
    totalSessions = 0
    for q in queryTwo:
        totalSessions += int(q['TotalSessions'])

    totalPaidVisits = db.data.aggregate(
        [{'$group': {'_id': None, 'total': {'$sum': '$PaidVisits'}}}]
    )
    teacherList = list(query)

    uniqueTeachers = db.data.find({}).distinct("Teacher")
    uniqueStudios = db.data.find({}).distinct("Studio")

    #get the top 5 teachers in each studio


    return render_template('index.html',
    query=query, teacherList=teacherList, totalSessions=totalSessions, uniqueStudios=uniqueStudios, totalPaidVisits=totalPaidVisits)


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

@app.route('/get-classes', methods=['POST', 'GET'])
def get_classes():
    service = ClassServiceCalls()
    response = service.GetClasses()

    #======
    # from suds.sudsobject import asdict
    #
    # def recursive_asdict(d):
    #     """Convert Suds object into serializable format."""
    #     out = {}
    #     for k, v in asdict(d).iteritems():
    #         if hasattr(v, '__keylist__'):
    #             out[k] = recursive_asdict(v)
    #         elif isinstance(v, list):
    #             out[k] = []
    #             for item in v:
    #                 if hasattr(item, '__keylist__'):
    #                     out[k].append(recursive_asdict(item))
    #                 else:
    #                     out[k].append(item)
    #         else:
    #             out[k] = v
    #     return out
    #
    # def suds_to_json(data):
    #     return json.dumps(recursive_asdict(data), default=json_util.default)
    #========

    dictResponse = suds_to_json(response)
    return dictResponse

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
