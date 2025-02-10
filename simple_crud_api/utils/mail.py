from importlib import import_module

from flask_mail import Message

from ..database import db_session
from ..models.user import User


simple_crud_api = import_module("simple_crud_api")

def send_account_activation_mail(recipients: str, message: str):
    try:
        msg = Message(
        'Flask: User account activation',
        recipients=[recipients],
        body=message
        )
        simple_crud_api.mail.send(msg)
        return True
    
    except Exception as e:
        return False

def send_password_reset_mail(recipients: str, message: str):
    try:
        msg = Message(
        'Flask: Password reset',
        recipients=[recipients],
        body=message
        )
        simple_crud_api.mail.send(msg)
        return True
    
    except Exception as e:
        return False
    

def check_mail_exists(mail_address: str) -> bool:
    users = db_session.query(User).filter_by(email=mail_address).all()
    if len(users) == 0:
        return False
    return True

def check_username_exists(username: str) -> bool:
    users = db_session.query(User).filter_by(username=username).all()
    if len(users) == 0:
        return False
    return True

def check_phone_exists(phone: int) -> bool:
    users = db_session.query(User).filter_by(phone=phone).all()
    if len(users) == 0:
        return False
    return True