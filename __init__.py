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
from datetime import datetime

#objects made by me
from objects.Utilities import Utilities
from objects.SudsConverter import SudsConverter
from objects.CSVImporter import CSVImporter
from objects.Queries import Queries
from objects.DictionaryBuilder import DictionaryBuilder


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
        query = queries.baseQuery(studio)

        # total sessions sum
        totalSessions = queries.totalSessions(studio)

        #total paid visits
        totalPaidVisits = queries.totalPaidVisits(studio)

        #total list of teachers
        teacherList = list(query)

        # topInstructors = queries.topInstructors()
        topInstructors = list(queries.topInstructors(studio))

        #totalSessionsPerStudio
        totalSessionsPerStudio = list(queries.totalSessionsPerStudio(studio))

        #topTeacher
        topTeacher = queries.topTeacher(studio)

        #topStudio
        # topStudio = queries.topStudio(studio)
        # for t in topStudio:
        #     print t

        # #Top Studio
        # t = list(queries.totalSessionsPerStudio())
        # print t


        uniqueStudios = queries.uniqueStudios(studio)
        uniqueTeachers = db.data.find({}).distinct("teacher")


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

@app.route('/mindbody/update-credentials', methods=['POST', 'GET'])
def mindbody_update_credentials():
    if not session.get('logged_in'):
        session.clear()
        return render_template('login.html')

    elif session['logged_in'] == True:
        form_username = str(request.form['username'])
        form_password = str(request.form['password'])
        form_siteid= str(request.form['siteid'])

        encrypted_pw = util.encode_password(form_password)
        decrypted_pw = util.decode_password(encrypted_pw)

        print encrypted_pw, decrypted_pw

        return render_template('mind-body.html')


@app.route('/import-data/mindbody/get-classes', methods=['POST', 'GET'])
def import_data_mindbody_classes():

    if not session.get('logged_in'):
        session.clear()
        return render_template('login.html')

    elif session['logged_in'] == True:

    #get form data

        USER_NAME = str(request.form['username'])
        USER_PASSWORD = str(request.form['password'])
        # SITE_IDS= str(request.form['siteid'])

        # USER_NAME = "Siteowner"
        # USER_PASSWORD = "apitest1234"
        SITE_IDS = [-99]

        dictionaryBuilder = DictionaryBuilder(USER_NAME, USER_PASSWORD, SITE_IDS)
        fullDict = dictionaryBuilder.buildClientDict()

        print fullDict[1]

        return fullDict

        # except Exception as e:
        #     return e

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
