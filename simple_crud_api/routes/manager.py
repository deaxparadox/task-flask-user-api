from flask import (
    Blueprint,
    jsonify,
    request
)
from flask.views import (
    MethodView
)
from flask_jwt_extended import (
    current_user, 
    jwt_required
)

from ..models.user import User
from ..database import db_session
from ..utils.user import UserType

bp = Blueprint("manager", __name__, url_prefix="/api/manager")

class ManagerView(MethodView):
    def __init__(self):
        self.db_session = db_session
    
    @jwt_required()
    def get(self):
        if current_user.role != UserType.Manager:
            return jsonify(message="Access denied"), 403
        employee = self.db_session.query(User).filter_by(role=UserType.Employee.value).all()
        team_lead = self.db_session.query(User).filter_by(role=UserType.TeamLead.value).all()
        data = {
            "employees": [user.to_dict() for user in employee],
            "team_leads": [tl.to_dict() for tl in team_lead]
        }
        return jsonify(data), 200
    
bp.add_url_rule("", view_func=ManagerView.as_view(name="manage-view"))