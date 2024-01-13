from models import *

class Appointment:
    appointment_id = AppointmentTable().getAppointmentID() + 1
    def __init__(self,
                 appointment_id,
                 clinic_id,
                 user_id,
                 date_time,
                 status):
        
        self.appointment_id = appointment_id
        self.clinic_id      = clinic_id
        self.user_id        = user_id
        self.date_time      = date_time
        self.status         = status
        
    @staticmethod
    def registerPatient(      clinic_id,
                              user_id,
                              date_time,
                              status):
        # Collecting items
        items = [
                              Appointment.appointment_id,
                              clinic_id,
                              user_id,
                              date_time,
                              status
        ]
        # Saving appointment
        appointment = Appointment(
                              Appointment.appointment_id,
                              clinic_id,
                              user_id,
                              date_time,
                              status)
        # Adding to table
        creeated = AppointmentTable().add(items)
        if creeated:
            Notification(items[2], f'your visit has been created and your appointment id is {Appointment.appointment_id}')
            # Updating appointment id
            Appointment.appointment_id += 1
            return appointment
        else:
            return
        
        
    
    @staticmethod
    def cancelVisit(appointment_id):
        AppointmentTable().cancelAppointment(appointment_id)
    
    @staticmethod
    def reschedule(appointment_id, user_id, new_date_time):
        AppointmentTable().reschedule_appointment(appointment_id, user_id, new_date_time)
        