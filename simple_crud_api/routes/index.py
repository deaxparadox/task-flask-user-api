from importlib import import_module

import click
from faker import Faker
from flask import (
    Blueprint,
    jsonify
)

from ..cache import cache
from ..models.user import User
from ..utils.user import UserType
from ..database import db_session


fake = Faker()
password = User.make_passsword("qwerQWER1234")

bp = Blueprint("index", __name__, url_prefix="/")


@bp.get("")
def hello():
    return jsonify(message="Hello to Flask API")


@bp.cli.command("hello")
def hello():
    print("hello to every one")
    
    
@bp.cli.command("create-tl")
def create_tl():

    user = User(username="teamlead1",email="teamlead1@gmail", password=password)
    user.account_activation = True
    user.role = UserType.TeamLead
    db_session.add(user)
    db_session.commit()
    
    user = User(username="teamlead2",email="teamlead2@gmail", password=password)
    user.account_activation = True
    user.role = UserType.TeamLead
    db_session.add(user)
    db_session.commit()
    
    user = User(username="teamlead3",email="teamlead3@gmail", password=password)
    user.account_activation = True
    user.role = UserType.TeamLead
    db_session.add(user)
    db_session.commit()
    
@bp.cli.command('create-employee')
def create_employee():

    user = User(username="employee1",email="employee1@gmail", password=password)
    user.account_activation = True
    user.role = UserType.Employee
    db_session.add(user)
    db_session.commit()
    
    user = User(username="employee2",email="employee2@gmail", password=password)
    user.account_activation = True
    user.role = UserType.Employee
    db_session.add(user)
    db_session.commit()
    
    user = User(username="employee3",email="employee3@gmail", password=password)
    user.account_activation = True
    user.role = UserType.Employee
    db_session.add(user)
    db_session.commit()

    user = User(username="employee4",email="employee4@gmail", password=password)
    user.account_activation = True
    user.role = UserType.Employee
    db_session.add(user)
    db_session.commit()
    
    user = User(username="employee5",email="employee5@gmail", password=password)
    user.account_activation = True
    user.role = UserType.Employee
    db_session.add(user)
    db_session.commit()
    
    user = User(username="employee6",email="employee6@gmail", password=password)
    user.account_activation = True
    user.role = UserType.Employee
    db_session.add(user)
    db_session.commit()
    