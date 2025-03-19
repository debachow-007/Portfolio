import os
import datetime
from portfolio import mail
from flask_mail import Message  # type: ignore

def calculate_age():
    now = datetime.datetime.now()
    birthday = datetime.datetime(year=2001, month=9, day=26)
    age = now.year - birthday.year - ((now.month, now.day)<(birthday.month, birthday.day))
    return age

def send_email(visitor):
    try:
        msg = Message(subject=f"New Contact Form Submission", 
                        sender = os.getenv('MAIL_SENDER'),
                        recipients=["debachow007@hotmail.com"])
        msg.body = f'''Hello,
        
    You have a new contact form submission. 
    Here are the details: 

        Name: {visitor['name']}
        Email: {visitor['email']}
        Message: {visitor['message']}
        
    Have a good day.'''
        
        mail.send(msg)
        print("Email sent successfully")
        
    except Exception as e:
        print(e)

