import sqlite3 as sq
class NotificationTable:
  
    def __init__(self):
        self.conn = sq.connect('database.db')
        self.cur  = self.conn.cursor()
        self.createTable()
        
    def createTable(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS notification (
                                notification_id INTEGER PRIMARY KEY,
                                user_id,
                                date_time DATE,
                                message TEXT,
                                FOREIGN KEY(user_id) REFERENCES users(id)
                                )""")
        
    def add(self, items):
        # Inserting items
        self.cur.execute("""INSERT OR IGNORE INTO notification VALUES(?,?,?,?)""",
                        items)
        
        # Commit
        self.conn.commit()
        
class Notification:
    
    notification_id = 1
    def __init__(self, user_id, message):
        from datetime import datetime
        self.user_id = user_id
        self.message = message
        self.date    = datetime.now()
        self.send()

    def send(self):
        message_with_time = f"{self.message} [{self.date}]"
        message_with_id   = f"Notification ID: {self.notification_id}. {message_with_time}"
        final_message     = f"User ID: {self.user_id}. {message_with_id}"
        items             = [Notification.notification_id, self.user_id, self.date, self.message]
        
        # Add items in table
        NotificationTable().add(items)
        
        # Incereas notification id
        Notification.notification_id += 1
        
        # Sending message
        print(final_message)


#notification = Notification(1234, "Your registration was done")
#notification.send()