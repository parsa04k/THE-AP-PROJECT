from models import *
from Appointment import *
from User import *
from clinic import *
import requests
id_and_capacity = requests.get('http://127.0.0.1:5000/slots')
id_and_capacity = eval(id_and_capacity.text)
clinic1 = Clinic.AddClinic(1, 'Habibi'    , 'SUT'           , 'classified'         , 'IT & AP'         , True, int(id_and_capacity['1']))
clinic2 = Clinic.AddClinic(2, 'mahmoodi'  , 'G-Floor IE-SUT', 'next to the window' , 'anti-deppressing', True, int(id_and_capacity['2']))
clinic3 = Clinic.AddClinic(3, 'nikpour'   , 'CS-SUT'        , 'Quera'              , 'Chocolate milk'  , True, int(id_and_capacity['3']))
clinic4 = Clinic.AddClinic(4, 'zolfi'     , 'IE-SUT'        , 'real'               , 'Debugging'       , True, int(id_and_capacity['4']))
clinic5 = Clinic.AddClinic(5, 'hedesh'    , 'IE-SUT'        , 'real'               , 'lahje yazdi'     , True, int(id_and_capacity['4']))
clinic6 = Clinic.AddClinic(6, 'khormali'  , 'CS-SUT'        , 'None'               , 'Django'          , True, int(id_and_capacity['6']))
clinic7 = Clinic.AddClinic(7, 'bakhshi'   , 'GIT'           , 'None'               , 'Project'         , True, int(id_and_capacity['7']))

user = Patient.signup(1, 'ali', 'a@k.com', '1234', 'patient')

user.login('a@k.com','1234')

user.update('name', 'ali kaman')

user.addVisit(1, '15/2/2023')


user.addVisit(2 ,'16/2/2023')

user.addVisit(2, '17/2/2023')

user.cancel(3)
user.reschedule(2, '17/2/2023')
#user.showVisits()

#user.showHistory()
#====================================
employee = Employee.signup(2, 'amir', 'a@f.com', '12345', 'employee')
employee.clinic(2)

employee.login('a@f.com', '12345')

employee.FinishVisit(3)

employee.ChangeCapacity(20)
user.showHistory()
#clinic1.SetAvailability(False)
#clinic1.ViewAppointment()