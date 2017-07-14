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
from objects.Queries import Queries


app = Flask(__name__)

util = Utilities()
db = util.dbConfig()

queries = Queries()

app.secret_key = 'akshdjasdGHJsslkgajh'

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

@app.route('/')
def dashboardRouting():
    if not session.get('logged_in'):
        session.clear()
        return render_template('login.html')

    elif session['logged_in'] == True:
        return home()

@app.route('/')
def home():
    if not session.get('logged_in'):
        session.clear()
        return render_template('login.html')

    elif session['logged_in'] == True:

        #assign studio variable from session
        studio = session['studio']

        #base query
        query = db.data.find({"profile":studio})

        # total sessions sum
        totalSessions = queries.totalSessions()

        #total paid visits
        totalPaidVisits = queries.totalPaidVisits()

        #total list of teachers
        teacherList = list(query)


        # topInstructors = queries.topInstructors()
        topInstructors = list(queries.topInstructors())

        #totalSessionsPerStudio
        totalSessionsPerStudio = list(queries.totalSessionsPerStudio())

        #topTeacher
        topTeacher = queries.topTeacher()

        # #Top Studio
        # t = list(queries.totalSessionsPerStudio())
        # print t


        uniqueTeachers = db.data.find({}).distinct("teacher")
        uniqueStudios = db.data.find({}).distinct("studio")


        return render_template('index.html',
        query=query, teacherList=teacherList, totalSessions=totalSessions, uniqueStudios=uniqueStudios, totalPaidVisits=totalPaidVisits,
        topInstructors=topInstructors, totalSessionsPerStudio=totalSessionsPerStudio, topTeacher=topTeacher)

@app.route('/mind-body', methods=['POST', 'GET'])
def mind_body_page():
    if not session.get('logged_in'):
        session.clear()
        return render_template('login.html')

    elif session['logged_in'] == True:
        return render_template('mind-body.html')


@app.route('/import-data/mindbody/get-classes', methods=['POST', 'GET'])
def import_data_mindbody_classes():

    if not session.get('logged_in'):
        session.clear()
        return render_template('login.html')

    elif session['logged_in'] == True:

        #get form data

        service = ClassServiceCalls()
        response = service.GetClasses()

        classList = response.Classes.Class

        print classList[4]

        classDict = []
        for c in classList:
            d = {}
            d['class'] = {}
            d['class']['name'] = str(c.ClassDescription.Name)
            d['class']['studio'] = str(c.Location.Name)
            d['class']['city'] = str(c.Location.City)
            d['class']['program'] = str(c.ClassDescription.Program.Name)
            d['class']['type'] = str(c.ClassDescription.SessionType.Name)

            d['instructor'] = {}
            d['instructor']['firstname'] = str(c.Staff.FirstName)
            d['instructor']['lastname'] = str(c.Staff.FirstName)
            d['instructor']['status'] = str(c.Staff.IndependentContractor)

            d['values'] = {}
            d['values']['totalbooked'] = str(c.TotalBooked)
            d['values']['maxcapacity'] = str(c.MaxCapacity)

            classDict.append(d)
            #import to db

        classDict = json.dumps(classDict, ensure_ascii=False)

        return classDict

@app.route('/import-data/csv', methods=['POST', 'GET'])
def import_data_csv():
    if not session.get('logged_in'):
        session.clear()
        return render_template('login.html')

    elif session['logged_in'] == True:

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
