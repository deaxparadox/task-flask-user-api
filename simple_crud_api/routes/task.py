from flask import (
    Blueprint,
    jsonify,
    request
)
from flask_jwt_extended import (
    current_user,
    jwt_required,
)
from flask.views import MethodView

from ..cache import cache
from ..database import db_session
from ..models.user import User
from ..models.task import Task
from ..models.task import TaskStatus
from ..serializer.task import TaskCreateSerializer
from ..utils.mixins import UserVerifyMixin
from ..utils.user import UserType

bp = Blueprint("task" , __name__, url_prefix="/api/task")


class TaskMixin:
    
    def get_manager_task(self, task_id: int | None = None):
        if task_id:
            return db_session.query(self.task_model).filter_by(id=task_id, assigned_by_manager_id=self.current_user.id).one_or_none()
        return db_session.query(self.task_model).filter_by(assigned_by_manager_id=self.current_user.id).all()
    
    def get_team_lead_task(self, task_id: int | None = None):
        if task_id:
            return db_session.query(self.task_model).filter_by(id=task_id, assigned_by_team_lead_id=self.current_user.id).one_or_none()
        return db_session.query(self.task_model).filter_by(assigned_by_team_lead_id=self.current_user.id).all()
    
    def get_employee_task(self, task_id: int | None = None):
        if task_id:
            return db_session.query(self.task_model).filter_by(id=task_id, assigned_to_id=self.current_user.id).one_or_none()
        return db_session.query(self.task_model).filter_by(assigned_to_id=self.current_user.id).all()
    
    def get_task(self, task_id: int | None = None):
        if self.current_user.role == UserType.Manager:
            return self.get_manager_task(task_id)
        
        elif self.current_user.role == UserType.TeamLead:
            return self.get_team_lead_task(task_id)
        
        elif self.current_user.role == UserType.Employee:
            return self.get_employee_task(task_id)
        
    def set_current_user(self):
        self.current_user: User = current_user
        
    def build_response_data(self, task: list[Task] | Task):
        data = {
            "user_details": {
                "user_id": self.current_user.id,
                "role": self.current_user.role.value
            }
        }
        
        if isinstance(task, list):
            data.update({"tasks": [x.to_dict() for x in task]})
            return data
        
        data.update({"task": task.to_dict() if task else "Task doesn't exists"})
        return data
    
    def create_manager_task(self, task: TaskCreateSerializer):
        """
        This function only create task, it `doesn't` save it.
        """
        task = Task(description=task.description, body=task.body, assigned_by_manager_id=self.current_user.id)
        return task
    
    def create_team_lead_task(self, task: TaskCreateSerializer):
        """
        This function only create task, it `doesn't` save it.
        """
        task = Task(description=task.description, body=task.body, assigned_by_team_lead_id=self.current_user.id)
        return task
    
    def verify_team_lead(self, user_id):
        self.chec

class TaskGet(MethodView, TaskMixin):

    init_every_request = False
    
    def __init__(self, task: Task):
        self.task_model: Task = task
    
    @jwt_required()
    def get(self):
        """
        Get all tasks
        """
        
        self.set_current_user()
        
        tasks: list[Task] = self.get_task()
        data = self.build_response_data(tasks)
        
        return  jsonify(data), 200

    @jwt_required()
    def post(self):
        """
        Create a task.
        """
        
        self.set_current_user()
        
        try:
            task_serializer = TaskCreateSerializer(**request.json)
        except Exception as e:
            return jsonify(message=str(e)), 400
        
        # create team lead task
        if self.current_user.role == UserType.TeamLead:
            # create task
            task = self.create_team_lead_task(task_serializer)
            db_session.add(task)
            db_session.commit()
            
            data = self.build_response_data(task)
            
            return jsonify(message=data), 201
        
        # create manager task
        if self.current_user.role == UserType.Manager:
            # create task
            task = self.create_manager_task(task_serializer)
            db_session.add(task)
            db_session.commit()
            
            data = self.build_response_data(task)
            
            return jsonify(message=data)
        
        return jsonify(message="Access denied, not authorized to create task"), 401

class TaskDetail(MethodView, TaskMixin):
    
    init_every_request = False
    
    def __init__(self, task: Task):
        self.task_model: Task = task
        
    @jwt_required()
    def get(self, task_id: str):
        self.set_current_user()
        
        try:
            task: Task = self.get_task(task_id=int(task_id))
        except Exception as e:
            return jsonify(message="Invalid task ID"), 400  
        
        data = self.build_response_data(task)
        
        # not found
        if not task:
            return jsonify(data), 404
        
        return  jsonify(data), 302

class TaskAssign(MethodView, TaskMixin, UserVerifyMixin):
    
    def __init__(self, user_model: User, task_model: Task):
        self.user_model = user_model
        self.task_model = task_model
        self.db_session = db_session
    
    @jwt_required()
    def get(self, task_id: str, user_id: str):
        """
        Assign task.
        """
        
        self.set_current_user()
        
        try:
            task_id, user_id = int(task_id), int(user_id)
        except Exception as e:
            return jsonify(message=str(e)), 400
        
        if not self.check_user_by_id(int(user_id)):
            jsonify(message="User doesnot exists"), 400
            
        task: Task = self.get_task(task_id)
        
        if not task:
            return jsonify(message="Task not found"), 400
        
        if self.current_user.role == UserType.Employee:
            return jsonify(message="User not authorized to assign task."), 401
        
        if self.current_user.role == UserType.Manager:
            if self.checked_user.role == UserType.TeamLead:
                task.assigned_by_team_lead_id = self.checked_user.id
                self.db_session.add(task)
                self.db_session.commit()
                return jsonify(message=f"Task {task_id} assigned to Team lead {user_id}"), 200
            return jsonify(message=f"Team lead doesn't exist"), 400
        
        if self.current_user.role == UserType.TeamLead:
            if self.checked_user.role == UserType.Employee:
                task.assigned_to_id = self.checked_user.id
                self.db_session.add(task)
                self.db_session.commit()
                return jsonify(message=f"Task {task_id} assigned to Employee {user_id}"), 200
            return jsonify(message=f"Team lead doesn't exist"), 400
        
        return jsonify(message="Invalid request"), 400

bp.add_url_rule("", view_func=TaskGet.as_view("task-all", Task))
bp.add_url_rule("/<task_id>", view_func=TaskDetail.as_view("task-detail", Task))
bp.add_url_rule("/<task_id>/assign/<user_id>", view_func=TaskAssign.as_view("task-assign", User, Task))