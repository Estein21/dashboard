import csv
import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient
import os
import re
# import Utilities from Utilities
# 
# util = Utilities()
# db = util.dbConfig()

class CSVImporter:
    def __init__(self):
        pass

    def removeStuff(self,str):
        str = re.sub(re.compile(r'\s+'), '', str)
        newstr = re.sub(r'[^a-zA-Z0-9 ]',r'',str)
        return newstr

    def importCSVtoDB(self):
        for filename in os.listdir('/Users/ethan/Desktop/Explore/YogaApp/YogiCSV'):
            if filename.endswith('.csv'):
                justFileName = os.path.splitext(os.path.basename(filename))[0]
                studioName = filename.split(' ')[2]

                csvfile = open(justFileName + '.csv', 'r')
                reader = csv.DictReader( csvfile )

                header = ['Teacher','Paid Visits','Percent of Total Visits*', 'Unique Clients', 'Comp/Guest Visits', 'Total Visits','Total Sessions','Average']
                for each in reader:
                    row={}
                    for field in header:
                        if each[field].isdigit():
                            row[self.removeStuff(field)]=int(each[field])
                        else:
                            row[self.removeStuff(field)]=each[field]
                            row['Studio'] = studioName
                        print row

        return ''
                    # db.data.insert(row)
