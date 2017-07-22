from objects.ClassService import ClassServiceCalls
from objects.ClientService import ClientServiceCalls
from datetime import datetime
import dateutil.relativedelta

oneMonthAgo = datetime.today() + dateutil.relativedelta.relativedelta(months=-1)

class DictionaryBuilder:
    def __init__(self, USER_NAME,USER_PASSWORD,SITE_IDS):
        self.USER_NAME = USER_NAME
        self.USER_PASSWORD = USER_PASSWORD
        self.SITE_IDS = SITE_IDS

        pass

    def buildClassDict(self):

        ## Get classes by instructor and build dictionary
        classService = ClassServiceCalls()
        classResponse = classService.GetClasses(self.USER_NAME, self.USER_PASSWORD, self.SITE_IDS)
        classList = classResponse.Classes.Class

        classDict = []
        for c in classList:
            d = {}
            d['id'] = str(c.ID)
            d['class_name'] = str(c.ClassDescription.Name)
            d['class_studio'] = str(c.Location.Name)
            d['class_city'] = str(c.Location.City)
            d['class_program'] = str(c.ClassDescription.Program.Name)
            d['class_type'] = str(c.ClassDescription.SessionType.Name)
            d['class_id'] = str(c.ClassDescription.ID)
            ##class ID

            d['instructor_name'] = str(c.Staff.Name)
            d['instructor_id'] = str(c.Staff.ID)
            d['instructor_contractor'] = str(c.Staff.IndependentContractor)

            d['values_totalbooked'] = str(c.TotalBooked)
            d['values_maxcapacity'] = str(c.MaxCapacity)

            classDict.append(d)

        return classDict


    def buildClientDict(self):

        clientService = ClientServiceCalls()
        clientResponse = clientService.GetAllClients()
        clientList = clientResponse.Clients.Client

        clientDict = []
        for c in clientList:
            d = {}
            d['cust_id'] = str(c.ID)
            d['cust_name'] = str(c.FirstName) + ' ' + str(c.LastName)
            clientDict.append(d)

            clientResponseVisits = clientService.GetClientVisits(str(c.ID), oneMonthAgo, datetime.today())
            clientVisitsDict = []

            if clientResponseVisits.Visits:
                visitsList = clientResponseVisits.Visits.Visit
                for v in visitsList:
                    q = {}
                    q['cust_id'] = str(c.ID)
                    q['class_id'] = str(v.ClassID)
                    q['class_time'] = str(v.ClassID)
                    q['class_name'] = str(v.Name)
                    q['class_location'] = str(v.Location.Name)
                    q['class_instructor_id'] = str(v.Staff.ID)
                    q['class_instructor_name'] = str(v.Staff.Name)

                    clientVisitsDict.append(q)

        return 'clientVisitsDict'
