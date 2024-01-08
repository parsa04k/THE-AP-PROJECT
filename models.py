"""to use and find the models you want:
    UserTable line 11 -----------------  AppointmentTable line 82 ----------------------------------- ClinicTable line 200
        register    -> line 28              add        -> line 103      validate_user -> line 158       register -> line 218    
        login       -> line 36              cancel     -> line 111      show visits   -> line 170       update   -> line 226
        update      -> line 53              replace    -> line 117      show history  -> line 182       view app -> line 239
        check login -> line 66              reschedule -> line 136                                      available-> line 250
"""
import sqlite3 as sq
import hashlib
from notif import *
class UserTable:
    
    def __init__(self):
        self.conn = sq.connect('database.db')
        self.cur  = self.conn.cursor()
        self.createTable()
        
    # Creating a user table that save the info of every person inside
    def createTable(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                email TEXT UNIQUE,
                                password TEXT,
                                islogged BOOLEAN,
                                roles TEXT CHECK( roles IN ('patient', 'employee') )
                                )""")
                            
    def register(self, items):
        
        # Hashing the password (the password is the 4th prop in the items)
        password_hash = hashlib.sha256(items[3].encode()).hexdigest()
        
        # Replacing the password with the hashed version
        items[3]      = password_hash
        
        # Getting info
        self.cur.execute("""INSERT OR IGNORE INTO users VALUES(?,?,?,?,?,?)""", items)
        
        self.conn.commit()
        
    def login(self, email, password):
        
        # Hash the provided password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Query the database for the user with the given email
        self.cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = self.cur.fetchone()
        
        if user is not None and user[3] == password_hash:
            # Change the islogged to true (user[0] is the user's id )
            self.cur.execute("UPDATE users SET islogged = ? WHERE id = ?",
                             (True, user[0]))
            
            # Commiting the changes
            self.conn.commit()

            # Return T/F to check if the user is already logged
            return True
        else:
            return False
        
    def checkLogin(self, id):
        # Check islogged in db for the selected user
        self.cur.execute("SELECT islogged FROM users WHERE id = ?", (id,))
        islogged = self.cur.fetchone()[0]
        
        # Check if the user exists
        if islogged is None:
            return Notification(id, "this id does not exist")
        else:
            return islogged
        
    def updateInfo(self, id, prop, new_value):
        # Check if the prop is valid
        props = ['name', 'email', 'password', 'islogged']
        if prop not in props:
            Notification(id, f'Invalid field: {prop}. Valid fields are {props}.')
            return False
        elif prop == 'login':
            new_value = hashlib.sha256(new_value.encode()).hexdigest()

        # Update the inputed info
        self.cur.execute(f"UPDATE users SET {prop} = ? WHERE id = ?",
                         (new_value, id))
        
        # Commiting the chanes
        self.conn.commit()
        return True
    
    def findUser(self, email):
        self.cur.execute("SELECT * FROM users WHERE email = ?",(email,))
        user = self.cur.fetchone()
        print(user)
        return user
    
    def showAllVisits(self, user_id):
        # Query the database for the appointment with all the users
        self.cur.execute("SELECT * FROM appointments WHERE user_id = ?",(user_id,))
        appointments = self.cur.fetchall()
        
        # If the user has appointments
        if appointments:
            return f'(appointment id, clinic_id, user_id, date, status) =>' ,appointments
        
        # If the user doesn't have any visits
        else:
            return Notification(user_id, 'No appointments found for this user.')
        
    def showHistory(self, user_id):
        # Query the database for the appointments with the given user_id
        self.cur.execute("SELECT * FROM appointments WHERE user_id = ? AND status = 'finished'",
                         (user_id,))
        appointments = self.cur.fetchall()

        # If the user has appointments
        if appointments:
            return appointments
        
        # If the user doesn't have any history
        else:
            Notification(user_id, 'No appointments found for this user.')
            return
        
        
    # Not recommended for large data
    def read(self):
        self.cur.execute("""SELECT * FROM users""")
        rows = self.cur.fetchall()
        return rows
    
class ClinicTable:
    
    def __init__(self):
        self.conn = sq.connect('database.db')
        self.cur  = self.conn.cursor()
        self.createTable()
        
    # Creating a user table that save the info of every person inside
    def createTable(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS clinics(
                                clinic_id INTEGER PRIMARY KEY,
                                name TEXT,
                                address TEXT,
                                clinic_info TEXT,
                                services TEXT,
                                availability BOOLEAN,
                                capacity INTEGER
                                )""")
        
    def register(self, items):
        # Getting info
        self.cur.execute("""INSERT OR IGNORE INTO clinics VALUES(?,?,?,?,?,?,?)""", items)
        
        # Commit them
        self.conn.commit()
        
    def updateInfo(self, clinic_id, prop, new_value):
        # First: Check if the prop is valid
        props = ['name', 'address', 'cantact_info', 'services','availability','capacity']
        if prop not in props:
            return Notification("None", """please choose one of these properties:
                                           ['name', 'address', 'cantact_info', 'services','availability','capacity']""")

        # Second: Update the inputed info
        self.cur.execute(f"UPDATE clinics SET {prop} = ? WHERE clinic_id = ?",
                         (new_value, clinic_id))
        # Third: Commiting the chanes
        self.conn.commit()
        Notification('None', 'capacity have changed')
        
    def viewAppointments(self, clinic_id):
        # First: Query the database for the appointments with the given clinic_id
        self.cur.execute("SELECT * FROM appointments WHERE clinic_id = ?", (clinic_id,))
        appointments = self.cur.fetchall()

        # Second: If the clinic has appointments
        if appointments:
            return appointments
        else:
            return Notification('None', 'No appointments found for this clinic.')
        
    def checkAvailability(self, clinic_id):
        # First: Get the avaibility of the clinic in the database
        self.cur.execute("SELECT capacity FROM clinics WHERE clinic_id = ?", (clinic_id,))
        capacity = self.cur.fetchone()[0]
        
        # Second: if the clinic is avaiable return T/F to check in adding visits
        if capacity > 0:
            return True
        else:
            return False
    
    def showVisits(self, emp_id, clinic_id):
        # First: Query the database for the appointment with all the users
        self.cur.execute("SELECT * FROM appointments WHERE clinic_id = ?",(clinic_id,))
        appointments = self.cur.fetchall()
        
        # Second: If the clinics has appointments
        if appointments:
            return appointments
        else:
            return Notification(emp_id, 'No appointments found for this clinic.')
    
    def Names(self):
        self.cur.execute("SELECT name FROM clinics")
        names = self.cur.fetchall()
        return names
    
    # Not recommended for large data
    def read(self):
        self.cur.execute("SELECT * FROM clinics")
        rows = self.cur.fetchall()
        for row in rows:
            return print(f'id: {rows[0]}, name: {row[1]}')
    
     
class AppointmentTable:
    
    def __init__(self):
        self.conn = sq.connect('database.db')
        self.cur  = self.conn.cursor()
        self.createTable()
        
    def createTable(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS appointments (
                                appointment_id INTEGER PRIMARY KEY,
                                clinic_id INTEGER,
                                user_id INTEGER,
                                date_time DATE,
                                status TEXT CHECK( status IN ('occupied', 'available', 'finished')),
                                FOREIGN KEY(user_id) REFERENCES users(id)
                                FOREIGN KEY(clinic_id) REFERENCES clinics(clinic_id)
                                )""")
        
    def add(self, items):
        # First: Check availability
        if not ClinicTable().checkAvailability(items[1]):
            Notification(items[2], "the clinic isn't available")
            return False
        
        # Second: Query the databsse to check if the appointment already exist
        self.cur.execute("SELECT EXISTS(SELECT * FROM appointments WHERE appointment_id = ?)", (items[0],))
        exists = self.cur.fetchone()[0]
        
        # Second(Part2)
        if exists:
            Notification(items[2], 'you already registered this visit')
            return False
        
        # Third: Inserting info to database
        self.cur.execute("""INSERT OR IGNORE INTO appointments VALUES(?,?,?,?,?)""",
                        items)
        
        # Fourth: Getting clinic id
        clinic_id = int(items[1])
        
        # Fifth: Selecting the clinic to decrease capacity
        self.cur.execute("SELECT capacity FROM clinics WHERE clinic_id = ?",
                            (clinic_id,))
        capacity = self.cur.fetchone()
        
        # Sixth: Decreasing the capacity
        self.cur.execute("UPDATE clinics SET capacity = ? WHERE clinic_id = ?",
                        (capacity[0] - 1, clinic_id))
        
        # Seventh: Checking availability after decreasing capacity
        if capacity[0] - 1 == 0:
            self.cur.execute("UPDATE clinics SET availability = False WHERE clinic_id=?",
                                (clinic_id,))
            
        # Commit the changes
        self.conn.commit()
        return True
        
        
        
        
    def cancelAppointment(self, appointment_id):
        # First: Check if the appointment already exist
        self.cur.execute("SELECT EXISTS(SELECT * FROM appointments WHERE appointment_id = ?)", (appointment_id,))
        exists = self.cur.fetchone()[0]
        if not exists:
            return print ('kkkk')
        
        # Second: Update the user_id and status fields for the appointment with the given id
        self.cur.execute("UPDATE appointments SET user_id = ?, status = ? WHERE appointment_id = ?",
                                                    # |             |                   |
                                                    # V             V                   V
                                                    (None,     'available',      appointment_id))
        
        # Third: Select appointment to get the clinic id
        self.cur.execute("SELECT clinic_id FROM appointments WHERE appointment_id = ?", (appointment_id,))
        clinic_id = self.cur.fetchone()[0]
        
        # Fourth: If the capacity was zero before change the availability
        if not ClinicTable().checkAvailability(clinic_id):
            ClinicTable().updateInfo(clinic_id, 'availability', True)
            
        # Fifth: Increasing the capacity
        self.cur.execute("UPDATE clinics SET capacity = capacity + 1 WHERE clinic_id = ?", (clinic_id,))
        
        # Commit the changes
        self.conn.commit()
        return True
        
    def reschedule_appointment(self, appointment_id, user_id, new_date_time):
        # First: Query the database for the appointment with the given id                      
        self.cur.execute("SELECT * FROM appointments WHERE appointment_id = ?",         
                         (appointment_id,))                                             
        old_appointment = self.cur.fetchone()                                           
                                                                                         
        # Second: If the appointment DOESNT exists                                              
        if old_appointment is None:
            return Notification(user_id, 'Appointment does not exist.')

        # Third: Check the new appointment is avaiable
        self.cur.execute("SELECT * FROM appointments WHERE date_time = ? AND status = 'available'",
                            (new_date_time,))
        new_appointment = self.cur.fetchone()
        
        # Third(part2):
        if new_appointment is None:
            return Notification(user_id, 'no available appointments for this time')
        
        # Fourth: Not the same clinics
        if old_appointment[1] != new_appointment[1]:
            if ClinicTable().checkAvailability(new_appointment[1]):
                self.cur.execute("UPDATE clinics SET capacity = capacity +1 WHERE clinic_id = ?",
                            (old_appointment[1],))
                self.cur.execute("UPDATE clinics SET capacity = capacity -1 WHERE clinic_id = ?",
                            (new_appointment[1],))
            else:
                return Notification(user_id, "the clinic that you selected isn't available")
            
        # Fifth: Change the old time
        self.cur.execute("UPDATE appointments SET user_id = ?, status = ? WHERE appointment_id = ?",
                         (None, 'available', appointment_id))
        
        # Sixth: Choose the new time
        self.cur.execute("UPDATE appointments SET user_id = ?, status = ? WHERE date_time = ?",
                         (user_id, 'occupied', new_date_time))
        
        # Commit the changes
        self.conn.commit()
        
        
    def validate(self, user_id, appointment_id):
        'this will check if the appointment does belong to the user or not'
        
        # First: Query the database for the appointment with the given id
        self.cur.execute("SELECT user_id FROM appointments WHERE appointment_id = ?",
                         (appointment_id,))
        appointment = self.cur.fetchone()

        # Second: If the appointment exists and the user_id matches
        if appointment is not None and appointment[0] == user_id:
            return True
        else:
            return Notification(user_id, 'this appointment does not belong to you')
        
    def DoneVisit(self, emp_id, clinic_id, appointment_id):
        # First: Query the database to find if the clinic exists or does not belong to the employee
        self.cur.execute("SELECT clinic_id FROM appointments WHERE appointment_id =?",(appointment_id,))
        clinic = self.cur.fetchone()
        if clinic is None:
            return Notification(emp_id, 'this clinic id doesnt exist')
        elif clinic[0] != clinic_id:
            return Notification(emp_id, 'this clinic is not yours')
        
        # Second: Finish the visit for the Patient
        self.cur.execute("UPDATE appointments SET status = ? WHERE appointment_id = ?",
                        ('finished', appointment_id,))
        
        self.conn.commit()
        
        Notification(emp_id, 'visit has been finished')
        
    def showAppointments(self, user_id):
        
        # First: Query the database for the appointments with the given user_id
        self.cur.execute("SELECT * FROM appointments WHERE user_id = ? AND status = 'occupied'",
                         (user_id,))
        appointments = self.cur.fetchall()
        

        # Second: Select each appointment with its clinic name and date
        for appointment in appointments:
                if appointment:
                    self.cur.execute("SELECT * FROM clinics WHERE clinic_id = ?",
                            (appointment[1],))
                    clinic = self.cur.fetchone()
                    print(f'clinic name: {clinic[1]}, date time: {appointment[3]}')
                else:
                    break
        
    def read(self):
        self.cur.execute("""SELECT * FROM appointments""")
        rows = self.cur.fetchall()
        return rows
    
    

    
    
