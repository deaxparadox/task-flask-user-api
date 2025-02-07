from collections import OrderedDict

from flask import (
    jsonify,
    Blueprint,
    request
)
from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    jwt_required
)

from ..serializer import (
    UserRegisterSerializer, 
    UserLoginSerializer
)
from ..utils.user import UserType
from ..database import db_session
from ..models.user import User


bp = Blueprint("auth", __name__, url_prefix="/api/auth")


class RegisterView(MethodView):
    init_every_request = False
    
    def __init__(self, model):
        self.model: User = model
        
    def check_user_exists(self, username: str) -> bool:
        query = db_session.query(User).where(self.model.username==username).all()
        if len(query) > 0:
            return True
        return False
    
    def get_user_type(self, value):
        """
        Return appropriate User roles
        """
        if UserType.Employee.value == value:
            return UserType.Employee
        if UserType.TeamLead.value == value:
            return UserType.TeamLead
        if UserType.Manager.value == value:
            return UserType.Manager
        return 0
    
    def post(self):
        try:
            serializer = UserRegisterSerializer(**request.json)
        except (AttributeError, TypeError) as e:
            # generated by serialier
            return jsonify(message="Invalid fields username, role"), 400
        
        # check user existence
        if self.check_user_exists(serializer.username):
            return jsonify(message="User name taken"), 302
        
        # check password length
        if len(serializer.password) < 8:
            return jsonify(message="Password must be atleast digit"), 400
        
        # check user role
        user_role = self.get_user_type(serializer.role)
        if not user_role:
            return jsonify(message="Invalid user role."), 400
        
        # add user
        user = self.model(
            username=serializer.username, 
            password=User.make_passsword(serializer.password),
        )
        user.role = user_role
        db_session.add(user)
        db_session.commit()
        
        return jsonify(message="User created successfully"), 201
    
class LoginView(MethodView):
    def __init__(self, model):
        self.model = model
        
    def post(self):
        
        try:
            serializer = UserLoginSerializer(**request.json)
        except (AttributeError, TypeError) as e:
            # generated by serialier
            return jsonify(message="Required username and password"), 400
        
        # get user
        user = db_session.query(User).filter(User.username==serializer.username).one_or_none()
        if not user or not user.active:
            return jsonify(message="User not found"), 404
        
        if not user.check_password(serializer.password):
            return jsonify(message="Invalid username and password"), 400
        
        data = OrderedDict()
        data["message"] = "User successfully logged in"
        data["access_token"] = create_access_token(identity=user, fresh=True)
        data["refresh_token"] = create_refresh_token(identity=user)
        
        return jsonify(data), 200


def register_api(app: Blueprint, model: User, name: str, view_class=None):
    app.add_url_rule(
        f'/{name}', 
        view_func=view_class.as_view(f"user-{name}", model)
    )
        

register_api(bp, User, 'register', RegisterView)
register_api(bp, User, 'login', LoginView)


@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh_token():
    """
    Refresh user token
    """
    identity = get_jwt_identity()
    
    user = db_session.query(User).filter_by(id=int(identity)).one_or_none()
    if not user:
        return jsonify(message="Invalid refresh token"), 401
    
    access_token = create_access_token(identity=user, fresh=False)
    
    return jsonify(access_token=access_token)