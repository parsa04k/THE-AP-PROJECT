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
        Notification.notification_id += 1
        print(final_message)


#notification = Notification(1234, "Your registration was done")
#notification.send()