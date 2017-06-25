from pymongo import MongoClient, GEO2D

mindBodyKey = 'he1mbH0lJxucXKUPpWrvT5vIN1c='



# def GetClientsByString(self, searchStr):
#         request = self.CreateBasicRequest("GetClientsRequest")
#
#         request.SearchText = searchStr
#         request.CurrentPageIndex = 1 # increase this number by one each time
#
#         return self.service.service.GetClients(request)

class Util:
    def __init__(self):
        pass
    def dbConfig(self):
        db = MongoClient('52.15.58.213', 27017).test
        return db
