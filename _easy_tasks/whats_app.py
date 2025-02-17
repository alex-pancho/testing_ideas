# Let's say that WhatsApp introduced a new feature - "Scheduled Send",
# which allows sending a message at a scheduled time.
# How would you test such a feature completely?
 
import datetime
import pytest
 
 
class User:
    def __init__(self, phone_number: str):
        self.phone_number = phone_number
        self.profile_picture = None
 
 
class WhatsApp:
    def __init__(self, phone_number: str):
        self.me = User(phone_number)
        self.contacts = []
        self.conversations = []
        self.scheduled_messages = []
 
    def send_message(self, text: str, recipient: User,
                     timestamp: datetime.datetime = None) -> int:
        """
        Schedules or sends a message to a recipient.
        Returns message ID.
        """
        if timestamp and timestamp <= datetime.datetime.now():
            raise ValueError("Scheduled time must be in the future.")
 
        message = {
            "id": len(self.scheduled_messages) + 1,
            "text": text,
            "recipient": recipient.phone_number,
            "timestamp": timestamp,
            "status": "scheduled" if timestamp else "sent"
        }
        self.scheduled_messages.append(message)
        return message["id"]
 
    def get_last_msg_status(self, message_id: int) -> str:
        """
        Returns the status of a message by ID.
        """
        for msg in self.scheduled_messages:
            if msg["id"] == message_id:
                return msg["status"]
        return "unknown"
 
    def cancel_message(self, message_id: int) -> bool:
        """
        Cancels a scheduled message.
        Returns True if successful, False otherwise.
        """
        for msg in self.scheduled_messages:
            if msg["id"] == message_id and msg["status"] == "scheduled":
                self.scheduled_messages.remove(msg)
                return True
        return False
    
def test_send_message():
    phone_number="+380951112233"
    w_app = WhatsApp(phone_number)
    recipient = User(phone_number="+380951112244")
    text = "Hello"
    time = datetime.datetime.now()
    msg_id = w_app.send_message(text, recipient, time)
    assert isinstance(msg_id, int)
    assert msg_id > 0
