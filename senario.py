from models import *
from User import *
from clinic import *
from Appointment import *
from notif import *
from function import *
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



print("""hello, welcome to the medical appointment system.
to use our services please write this specific commands that we made for you

to sign up enter ..............'register' 
to login enter ................'login'
to logout enter ...............'logout'
to update your user info enter 'update'
to show your visits enter .....'show visits'
to show visit history enter ...'history'
to add a visit enter ..........'add visit'
to cancel any visit enter .....'cancel visit'
to reschedule visit enter .....'reschedule'

if you are an employee you can use this commands:

to see patients visits enter ......'current visits'
to delete any patients visit enter 'delete visit'
to incereas visits enter ..........'incereas visits'
""")
u = Patient.signup(21,"akbar","l@l.com","123","patient",None)
u.login("l@l.com","123")
u.addVisit(1,"1/8/2023")

while True:
    command = input('wtite comand: ')

    if command == 'register':
        print('''please enter this things:''')
        
        # register user
        id = int(input('write id(must be number): '))
        name = input('write name: ')
        email = input('write email: ')
        password = input('write password: ')
        role = input('select your role[patient or employee]: ')
        if role == 'patient':
            user = Patient.signup(id, name, email, password, 'patient',)
            print('your account have been created')

        elif role == 'employee':
            clinic_id = int(input('write your clinic_id: '))
            user = Employee.signup(id, name, email, password, 'employee', clinic_id)
            print('your account have been created')

        else:
            print('invalid role')
            
    elif command == 'login':
            email=input("write email: ")
            user = User.findUser(email)
                
            print('''please write how do you want to login into the system
                  1- use your normal password : write 'normal'
                  2- use temporary password :   write 'temporary''')
            cmd = input()
            
            if cmd == 'temporary':
                # Generating  a password
                code = generate_temp_password(8)
                print(f'here is the code that can help you login: {code}')
                
                # login with temporary password
                confirm =input("confirm the code that you got: ")
                if code == confirm:
                    new_password = input('write a new password: ')
                    print('-------------------')
                    user.NewPassword(new_password)
                    password=input("write your password: ")
                    
                    user.login(email, password)
                else:
                    print('invalid code')
                    
                
            else:
                password=input("write your password: ")
                user.login(email, password)
                
    elif command == 'update':
        # Selecting the info that want to change
        print('''if you want to update any info just write the thing that you want to change:
                 your options are:
                 1- name
                 2- password
                 3- email''')
        prop = input()
        
        # Giving a new value to the selected prop
        print('''write the new value that you want''')
        val = input()
        user.update(prop,val)
        
        # Changing info
        
    
    elif command == 'logout':
        user.logout()
    # logout
    
    elif command == 'show visits':
        if isinstance(user, Patient):
            pass
            # show visit
        else:
            print('you are not a patient')
    
    elif command == 'history':
        if isinstance(user, Patient):
            user.showHistory()
        # show history
        else:
            print('you are not a patient')

    elif command == 'add visit':
        if isinstance(user, Patient):
            clinic_id=input("write your clinic id: ")
            time = input("write the time: ")                  
            user.addVisit(clinic_id,time)
        # add isit for the user                                             
        else:
            Notification(user.id,'you are not a patient')      
            
    elif command == 'cancel visit':
        if isinstance(user, Patient):
            Appointmen_id=input("write your appointment id: ")
            user.cancel( Appointmen_id)     
        # cancel visit
        else:
           Notification(user.id,'you are not a patient')   
    
    elif command == 'reschedule':
        if isinstance(user, Patient):
            appointment_id=input("appointment_id: ")
            new_date_tim=input("time: ")
            user.reschedule()
        # reschedule visit
        else:
            print('you are not a patient')
    
    # edame dastoorat
    elif command=="current visits":
        if isinstance(user, Employee):
            user.showAllVisits()
        else:
            Notification(user.id, "you are not employee")
    
    elif command=='delete visit':                                   
        if isinstance(user, Employee):
            patient_id=int(input("wrtie patient id: "))
            appointment_id=int(input("write patient visit id: "))
            user.cancelPatientVisit(patient_id, appointment_id)
        else:
            Notification(user.id, "you are not employee")
        
    elif command=="incereas visits":
        if isinstance(user, Employee):
            new_capacity=int(input("enter new capacity: "))
            user.ChangeCapacity(new_capacity)
            
        else:
            Notification(user.id, "you are not employee")
        
    else:
        print('invalid command')