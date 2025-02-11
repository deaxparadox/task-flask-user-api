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
from ..serializer.task import (
    TaskCreateSerializer,
    TUESerializer,
    TUMSerializer
)
from ..utils.mixins import UserVerifyMixin
from ..utils.user import UserType


bp = Blueprint("task" , __name__, url_prefix="/api/task")


class TaskMixin:
    
    def get_manager_task(self, task_id: int | None = None):
        # manager will get all task.
        if task_id:
            return db_session.query(self.task_model).filter_by(id=task_id).one_or_none()
        return db_session.query(self.task_model).filter_by().all()
    
    def get_team_lead_task(self, task_id: int | None = None):
        if task_id:
            return db_session.query(self.task_model).filter_by(id=task_id, created_by_id=self.current_user.id).one_or_none()
        return db_session.query(self.task_model).filter_by(created_by_id=self.current_user.id).all()
    
    def get_employee_task(self, task_id: int | None = None):
        if task_id:
            return db_session.query(self.task_model).filter_by(id=task_id, assigned_to_id=self.current_user.id).one_or_none()
        return db_session.query(self.task_model).filter_by(assigned_to_id=self.current_user.id).all()
    
    def get_task(self, task_id: int | None = None):
        if self.current_user_role == UserType.Manager:
            return self.get_manager_task(task_id)
        
        elif self.current_user_role == UserType.TeamLead:
            return self.get_team_lead_task(task_id)
        
        elif self.current_user_role == UserType.Employee:
            return self.get_employee_task(task_id)
        
    def set_current_user(self):
        self.current_user: User = current_user
        self.current_user_role: UserType = current_user.role
        
    def build_response_data(self, task: list[Task] | Task):
        data = {}
        
        if isinstance(task, list):
            data.update({"tasks": [x.to_dict() for x in task], "total_task": len(task)})
            return data
        
        data.update({"task": task.to_dict() if task else "Task doesn't exists"})
        return data
    
    def create_manager_task(self, task: TaskCreateSerializer):
        """
        This function only create task, it `doesn't` save it.
        """
        task = Task(description=task.description, body=task.body, created_by_id=self.current_user.id)
        return task
    
    def create_team_lead_task(self, task: TaskCreateSerializer):
        """
        This function only create task, it `doesn't` save it.
        """
        task = Task(
            description=task.description, 
            body=task.body,
            created_by_id=self.current_user.id
        )
        return task
    
    def get_task_status(self, status: str):
        if TaskStatus.Completed.value == status:
            return TaskStatus.Completed
        elif TaskStatus.Done.value == status:
            return TaskStatus.Done
        elif TaskStatus.Inprogress.value == status:
            return TaskStatus.Inprogress
        elif TaskStatus.PendingReview.value == status:
            return TaskStatus.PendingReview
        elif TaskStatus.NotStarted.value == status:
            return TaskStatus.NotStarted
        return None
    
    def get_update_serializer(self):
        if self.current_user.role == UserType.Manager or self.current_user.role == UserType.TeamLead:
            return TUMSerializer
        return TUESerializer
    
    
    def check_task_created_by_team_lead(self, user_id):
        """
        This function receives the user_id from subject task.
        """
        return True if self.db_session.query(User).filter_by(id=user_id).one().role == UserType.TeamLead else False

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
        
        return jsonify(message="Access denied: not authorized"), 403


class TaskDetail(MethodView, TaskMixin):
    
    init_every_request = False
    
    def __init__(self, task: Task):
        self.task_model: Task = task
        self.db_session = db_session
        
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
    
    
    @jwt_required()
    def put(self, task_id: str):
        """
        Update a task
        """
        
        try:
            task_id=int(task_id)
        except Exception as e:
            jsonify(message=str(e)), 400
        
        self.set_current_user()
        
        try:
            serializer = self.get_update_serializer()(**request.json)
        except (AttributeError, TypeError) as e:
            return jsonify(message=str(e)), 400
        
        
        task = self.get_task(task_id)
        if not task:
            return jsonify(message="Task not found"), 404
        
        if self.current_user.role == UserType.Employee:
            # Employee can only update status of the task
            
            status = self.get_task_status(serializer.status)
            
            if not status: return jsonify(message="Invalid status"), 400
            
            if status == TaskStatus.PendingReview or status == TaskStatus.Done:
                return jsonify(message="Access denied: not authorized"), 403
            
            if status == TaskStatus.Completed:
                task.status = TaskStatus.PendingReview
                self.db_session.add(task)
                self.db_session.commit()
                return jsonify(message="Task status updated"), 202
            
            task.status = status
            self.db_session.add(task)
            self.db_session.commit()
            return jsonify(message="Task status updated"), 202
        
        if self.current_user.role == UserType.TeamLead:
            for k in serializer.__class__.__dict__.get("__match_args__"):
                value = getattr(serializer, k)
                if k == "status": 
                    value = self.get_task_status(value)
                    if not value: return jsonify(message="Invalid status"), 400
                if value:
                    setattr(task, k, value)
                    
            self.db_session.add(task)
            self.db_session.commit()
            
            return jsonify(message="Task updated successfully"), 202
        
        
        if self.current_user.role == UserType.Manager:
            for k in serializer.__class__.__dict__.get("__match_args__"):
                value = getattr(serializer, k)
                if k == "status": 
                    value = self.get_task_status(value)
                    if not value: return jsonify(message="Invalid status"), 400
                if value:
                    setattr(task, k, value)
                    
            self.db_session.add(task)
            self.db_session.commit()
            
            return jsonify(message="Task updated successfully"), 202
        
        return jsonify(message="Invalid request"), 404
    
    @jwt_required()
    def delete(self, task_id: str):
        """
        Delete a task.
        """
        
        self.set_current_user()
        
        if self.current_user_role == UserType.Employee:
            return jsonify(message="Access denied: not authorized"), 403
        
        try:
            task_id: int = int(task_id)
        except Exception as e:
            return jsonify(message=str(e)), 400

        # delete task
        task: Task = self.get_task(task_id)
        if not task:
            return jsonify(message="task not found"), 400
        
        if self.current_user_role == UserType.Manager:    
            task_data = {"task_id": task_id, "description": task.description}
            self.db_session.delete(task)
            self.db_session.commit()
            return jsonify(message="Task ({task_id}:{description}) delete successfully".format(**task_data)), 204
                
        if self.current_user_role == UserType.TeamLead:
            if task.created_by_id == self.current_user.id:
                task_data = {"task_id": task_id, "description": task.description}
                self.db_session.delete(task)
                self.db_session.commit()
                return jsonify(message="Task ({task_id}:{description}) delete successfully".format(**task_data)), 204
            return jsonify(message="Access denied: Unauthorized request"), 403
        return jsonify({}), 500

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
        
        if self.current_user.role == UserType.Employee:
            return jsonify(message="Access denied: not authorized"), 403
        
        try:
            task_id, user_id = int(task_id), int(user_id)
        except Exception as e:
            return jsonify(message=str(e)), 400
        
        # check employee existence before assign a task
        # and employee should be active
        if not self.check_user_by_id(int(user_id)):
            return jsonify(message="User doesnot exists"), 400

        task: Task = self.get_task(task_id)
        
        if not task:
            return jsonify(message="Task not found"), 400
        
        if self.current_user.role == UserType.Manager:
            # manager can assign to team lead and employee
            task.assigned_by_id = self.current_user.id
            task.assigned_to_id = self.checked_user.id
            self.db_session.add(task)
            self.db_session.commit()
            return jsonify(message=f"Manager -> Assigns ask {task_id} assigned to Team lead {user_id}"), 202
        
        if self.current_user.role == UserType.TeamLead:
            # team lead can assign to Employee
            
            if self.checked_user.role == UserType.Employee:
                task.assigned_by_id = self.current_user.id
                task.assigned_to_id = self.checked_user.id
                self.db_session.add(task)
                self.db_session.commit()
                return jsonify(message=f"Task {task_id} assigned to Employee {user_id}"), 200
            return jsonify(message=f"Team lead doesn't exist"), 400
        
        return jsonify(message="Invalid request"), 400


bp.add_url_rule("", view_func=TaskGet.as_view("task-all", Task))
bp.add_url_rule("/<task_id>", view_func=TaskDetail.as_view("task-detail", Task))
bp.add_url_rule("/<task_id>/assign/<user_id>", view_func=TaskAssign.as_view("task-assign", User, Task))