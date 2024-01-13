from models import *
from Appointment import *
from notif import *
from clinic import *
class User:
    
    def __init__(self,
                 id       : int,
                 name     : str,
                 email    : str,
                 password : str,
                 role     : ['employee','patient'],
                 clinic_id):
        self.id        = id
        self.name      = name
        self.email     = email
        self.password  = password
        self.role      = role
        self.clinic_id = clinic_id

    @classmethod
    def signup(cls,
               id       : int,
               name     : str,
               email    : str,
               password : str,
               role,
               clinic_id):
        
        # Collecting items
        items = [id, name, email, password, False, role, clinic_id]
        
        # registering and saving user in database
        UserTable().register(items)
        
        # saving user in class
        user = cls(id, name, email, password, role, clinic_id)
        Notification(id, 'account created!')
        return user
    
    @staticmethod
    def login(email, password):
        # Checking email and password in database
        if UserTable().login(email, password):
            user = UserTable().findUser(email)
            LoginTable().add(user[0])
            return Notification(user[0], 'logged into the account')
        else:
            user = UserTable().findUser(email)
            return Notification(user[0], 'incorrect email or password')
        
    def NewPassword(self, new_password):
        # Hash the new password
        new_password = hashlib.sha256(new_password.encode()).hexdigest()
        
        # Change the password in database
        UserTable().updateInfo(self.id, 'password', new_password)
        
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
        
    @staticmethod
    def findUser(email):
        # Check the email exist in database
        try:
            user_info = UserTable().findUser(email)
            # return user to use it in senario
            if str(user_info[5]) == 'patient':
                user = Patient(user_info[0], user_info[1], user_info[2], user_info[3], user_info[5], None)
                return user
            elif str(user_info[5]) == 'employee':
                user = Employee(user_info[0], user_info[1], user_info[2], user_info[3], user_info[5], user_info[6])
                return user
        except TypeError:
            return False
        
class Patient(User):
    
    def __init__(self, id, name, email, password, role, clinic_id):
        super().__init__(id, name, email, password, role, clinic_id)
    
    def addVisit(self, clinic_id, date_time):#------------------------->steps:
        # Check if the user is logged in                                    # 1- check login
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
                                                                                                                                                                      
        appointment = Appointment.registerPatient(clinic_id,
                                                  self.id,
                                                  date_time,
                                                  'occupied')
        
        
    def cancel(self, appointment_id):
        # Check if the user is logged in                                    
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
        
        # If appointment got canceled                                                                                                                               
        if AppointmentTable().cancelAppointment(appointment_id):
            return Notification(self.id, 'your appointment has been canceled')
        
        # If appointment doesn't exist
        elif AppointmentTable().cancelAppointment(appointment_id) is None:
            return Notification(self.id, 'this appointment does not exist')
        
        # if the visit already canceled
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
    
    def __init__(self, id, name, email, password, role, clinic_id):
        super().__init__(id, name, email, password, role, clinic_id)
        
    def showAllVisits(self):
        # Check if the user is logged in                                    
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system")
        Clinic().viewAppointments(self.clinic_id)
        
    def cancelPatientVisit(self, patient_id, appointment_id):
        # Check if the user is logged in                     
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
        
        # Check if the user id and the appointment id match                                                                                   
        if not AppointmentTable().validate(patient_id, appointment_id):
            return Notification(self.id,"this appointment doesn't belong to you")
        
        # Cencel the appointment
        Appointment.cancelVisit(appointment_id)
        Notification(self.id, f'the patient with this id: {patient_id} and this appointment id: {appointment_id} visit was canceled')
        
    def FinishVisit(self, appointment_id):
        # Check if the user is logged in
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
        
        # Finish the appointment status
        AppointmentTable().DoneVisit(self.id, self.clinic_id, appointment_id)
        
    def ChangeCapacity(self, new_capacity : int):
        # Check if the user islogged
        if not UserTable().checkLogin(self.id):
            return Notification(self.id, "you are not logged in to the system") 
        
        # Change the capacity in database
        ClinicTable().updateInfo(self.clinic_id, 'capacity', new_capacity)
        Notification(self.id, 'capacity have changed')

        

        
        
        