from pymongo import MongoClient, GEO2D

class Utilities:
    def __init__(self):
        pass

    def dbConfig(self):
        db = MongoClient('52.15.58.213', 27017).test
        return db

    def secretKey(self):
        key = 'akshdjasdGHJsslkgajh'
        return key
