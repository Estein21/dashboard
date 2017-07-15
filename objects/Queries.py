from pymongo import MongoClient, GEO2D
from Utilities import Utilities
import json

util = Utilities()
db = util.dbConfig()

class Queries:
    def __init__(self):
        pass

    def topInstructors(self,studio):

        #get the top 5 teachers in each studio
        topFiveTeachersPerStudio = db.data.aggregate([
            {'$match' : {'profile': studio}},
            {'$sort': { 'values.totalsessions': -1} },
            {
                '$group': {
                    '_id' :  '$studio',
                    'docs': {'$push': '$$ROOT' }
                }
            },
            {
                '$project': {
                    'topfive': {
                        '$slice': ['$docs', 6]
                    }
                }
            }
        ])

        topInstructors = []
        for t in topFiveTeachersPerStudio:
            for i in range(5):
                d = {}
                d['studio'] = t['topfive'][i]['studio']
                d['drilldown'] = t['topfive'][i]['teacher']
                d['teacher'] = t['topfive'][i]['teacher']
                d['totalsessions'] = t['topfive'][i]['values']['totalsessions']
                # d = json.dumps(d).encode('utf-8')
                # d = map(str, d)
                topInstructors.append(d)

        return topInstructors

    def totalSessions(self, studio):
        query = db.data.find({"profile":studio})
        totalSessions = 0
        for q in query:
            totalSessions += int(q['values']['totalsessions'])
        return totalSessions

    def totalSessionsPerStudio(self,studio):
        #get the top 5 teachers in each studio
        totalSessionsPerStudio = db.data.aggregate([
            {'$match' : {'profile': studio}},
            {
                '$group': {
                    '_id' :  '$studio',
                    'totalSessions': { '$sum': "$values.totalsessions"  }
                }
            }
        ])
        return totalSessionsPerStudio



    def totalPaidVisits(self, studio):
        totalPaidVisits = db.data.aggregate([
            {'$match' : {'profile': studio}},
            {'$group': {'_id': None, 'total': {'$sum': '$values.paidvisits'}}}
        ])
        return totalPaidVisits

    def topTeacher(self,studio):
        topTeacher = db.data.find_one(
            # {"profile":studio},
            # {'profile': studio},
            {'$query':{},'$orderby':{'values.totalsessions':-1}}

        )
        return topTeacher

    def topStudio(self,studio):
        topStudio = db.data.aggregate([
            {'$match' : {'profile': studio}},
            {
                '$group': {
                    '_id' :  '$studio',
                    'totalSessions': { '$sum': "$values.totalsessions"  }
                }
            }
        ])
        return topStudio

    def baseQuery(self, studio):
        baseQuery = db.data.find({"profile":studio})
        return baseQuery

    def uniqueStudios(self, studio):
        uniqueStudios = db.data.find({"profile":studio}).distinct("studio")
        return uniqueStudios
