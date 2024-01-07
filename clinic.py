from models import *

    #Defining The Class
class Clinic:
    def __init__(                  self,
                                   clinic_id,
                                   name,
                                   address,
                                   clinic_information,
                                   offered_services,
                                   availability,
                                   capacity):
    # Setting Properties
        self.clinic_id           = clinic_id
        self.name                = name
        self.adress              = address
        self.clinic_information  = clinic_information
        self.offered_services    = offered_services
        self.availabality        = availability
        self.capacity            = capacity
        
    # Adding Clinic
    @staticmethod
    def AddClinic(                 clinic_id,
                                   name,
                                   address, 
                                   clinic_information,
                                   offered_services, 
                                   availability,
                                   capacity):

        #Collecting Items
        items =  [               clinic_id,
                                   name, 
                                   address,
                                   clinic_information, 
                                   offered_services,
                                   availability,
                                   capacity]
        
        ClinicTable().register(items)
        clinic = Clinic(           clinic_id, 
                                   name, address, 
                                   clinic_information,
                                   offered_services, 
                                   availability,
                                   capacity)
        return clinic
    
    # Updating Clinic Information
    def UpdateClinicInfo(          self,
                                   id,
                                   prop,
                                   value):
        
        ClinicTable().updateInfo(  self.clinic_id ,
                                   id,
                                   prop, 
                                   value)

    # Setting Availibility
    def SetAvailability(self, on_or_off: bool):
        ClinicTable().updateInfo(self.clinic_id, 'availability', on_or_off)
                  
    # Viewing Appointment
    def ViewAppointment(self):
        ClinicTable().viewAppointments(self.clinic_id)
        
    @staticmethod
    def GetNames():
        return ClinicTable().Names()
        


      
    