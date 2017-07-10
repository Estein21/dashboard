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
from objects.SudsConverter import SudsConverter
from objects.CSVImporter import CSVImporter

app = Flask(__name__)

util = Utilities()
db = util.dbConfig()

app.secret_key = 'akshdjasdGHJsslkgajh'


@app.route('/')
def dashboardRouting():
    if not session.get('logged_in'):
        session.clear()
        return render_template('login.html')

    elif session['logged_in'] == True:
        return home()


@app.route('/')
def home():


    studio = session['studio']

    query = db.data.find({"profile":studio})

    # total sessions sum
    queryTwo = db.data.find()
    totalSessions = 0
    for q in queryTwo:
        totalSessions += int(q['values']['totalsessions'])

    totalPaidVisits = db.data.aggregate(
        [{'$group': {'_id': None, 'total': {'$sum': '$values.paidvisits'}}}]
    )
    teacherList = list(query)

    uniqueTeachers = db.data.find({}).distinct("teacher")
    uniqueStudios = db.data.find({}).distinct("studio")

    #get the top 5 teachers in each studio


    return render_template('index.html',
    query=query, teacherList=teacherList, totalSessions=totalSessions, uniqueStudios=uniqueStudios, totalPaidVisits=totalPaidVisits)

@app.route('/mindbody', methods=['POST', 'GET'])
def mind_body_page():
    return render_template()


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

@app.route('/import-data/mindbody/get-classes', methods=['POST', 'GET'])
def import_data_mindbody_classes():
    service = ClassServiceCalls()
    response = service.GetClasses()

    classList = response.Classes.Class

    classDict = []
    for c in classList:
        d = {}
        d['class'] = {}
        d['class']['name'] = str(c.ClassDescription.Name)
        d['class']['program'] = str(c.ClassDescription.Program.Name)
        d['class']['studio'] = str(c.Location.City)

        d['instructor'] = {}
        d['instructor']['firstname'] = str(c.Staff.FirstName)
        d['instructor']['lastname'] = str(c.Staff.FirstName)
        classDict.append(d)


    print classDict
    return ''

@app.route('/import-data/csv', methods=['POST', 'GET'])
def import_data_csv():

    #Import Header names from uploaded CSV per studio

    #Name studio

    #User selects Header names to import

    #Run upload script

    # CSVImporter = CSVImporter()


    return ''


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
