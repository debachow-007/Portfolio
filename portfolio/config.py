import os
from dotenv import load_dotenv # type: ignore

load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_SERVER = 'smtp.mailersend.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_SENDER')
    