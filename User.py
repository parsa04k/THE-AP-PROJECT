from models import *
from Appointment import *
from notif import *
class User:
    
    def __init__(self,
                 id       : int,
                 name     : str,
                 email    : str,
                 password : str,
                 role     : ['employee','patient']):
        self.id       = id
        self.name     = name
        self.email    = email
        self.password = password
        self.role     = role

    @classmethod
    def signup(cls,
               id       : int,
               name     : str,
               email    : str,
               password : str,
               role):
        
        # Collecting items
        items = [id, name, email, password, False, role]
        
        # registering and saving user in database
        UserTable().register(items)
        
        # saving user in class
        user = cls(id, name, email, password, role)
        Notification(id, 'account created!')
        return user
    
    @staticmethod
    def login(email, password):
        # Checking email and password in database
        if UserTable().login(email, password):
            return Notification('None', 'logged into the account')
        else:
            return Notification('None', 'incorrect email or password')
        
    def update(self, prop, new_value):
        # Check if the user is logged in
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system")         
        # Updating info
        if UserTable().updateInfo(self.id, prop, new_value):
            Notification(self.id, f'your {prop} have been changed to {new_value}')
        
    def logout(self):
        # Check if the user is logged in
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
                                                                                                  
        # Changing islogged to false
        if UserTable().updateInfo(self.id, 'islogged', False):
            return Notification(self.id, 'you have logged out!')
        
class Patient(User):
    
    def __init__(self, id, name, email, password, role):
        super().__init__(id, name, email, password, role)
    
    def addVisit(self, clinic_id, date_time):#------------------------->steps:
        # Check if the user is logged in                                    # 1- check login
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
                                                                                                                                                                      
        appointment = Appointment.registerPatient(clinic_id,
                                                  self.id,
                                                  date_time,
                                                  'occupied')
        
        
    def cancel(self, appointment_id):#--------------------------------->steps:
        # Check if the user is logged in                                    # 1- check login
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
                                                                                                                                                                              
        if   AppointmentTable().cancelAppointment(appointment_id):
                Notification(self.id, 'your appointment has been canceled')
                
        elif AppointmentTable().cancelAppointment(appointment_id)is None:
            return Notification(self.id, 'this appointment does not exist')
        
        else:
            Notification(self.id, 'visit already canceled')
        
    def reschedule(self, appointment_id, new_date_time):
        # Check if the user is logged in                            
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
                                                                                                                                                                      
        # check appointment id belonging
        if AppointmentTable().validate(self.id, appointment_id):
           Appointment.reschedule(appointment_id, self.id, new_date_time)
          
        else:
            return Notification(self.id, "this appointment doesn't belong to you")
        
    def showVisits(self):
        print(UserTable().showAllVisits(self.id))
        
    def showHistory(self):
        print(UserTable().showHistory(self.id))
        
class Employee(User):
    
    def __init__(self, id, name, email, password, role):
        super().__init__(id, name, email, password, role)
        
    def clinic(self, clinic_id):
        self.clinic_id = clinic_id
        
    def showAllVisits(self):#--------------------------------->steps:
        # Check if the user is logged in                                    # 1- check login
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system")
        ClinicTable().viewAppointments(self.clinic_id, self.id)
        
    def cancelPatientVisit(self, patient_id, appointment_id):#--------------------------------->steps:
        # Check if the user is logged in                                    # 1- check login
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
                                                                                           
        if not AppointmentTable().validate(patient_id, appointment_id):
            return Notification(self.id,"this appointment doesn't belong to you")
        
        Appointment.cancelVisit(appointment_id)
        
    def FinishVisit(self, appointment_id):
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
        AppointmentTable().DoneVisit(self.id, self.clinic_id, appointment_id)
        
    def ChangeCapacity(self, new_capacity : int):
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
        ClinicTable().updateInfo(self.clinic_id, 'capacity', new_capacity)
        

        
        
        