from sqlalchemy import (
    Boolean, 
    BigInteger,
    Column, 
    Enum,   
    Integer, 
    String,
)

from sqlalchemy.orm import relationship
from simple_crud_api.database import Base

from ..utils.security.passwd import generate_hashed_password, check_password
from ..utils.user import UserType

class User(Base):
    __tablename__ = "user"
    
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(1000))
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)
    role = Column(Enum(UserType), default=UserType.Employee)
    email = Column(String(120), nullable=True)
    phone = Column(BigInteger, nullable=True)
    
    address = relationship(
        "Address", 
        uselist=False,
        cascade="save-update",
        passive_deletes=True,
        back_populates="user"
    )
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def set_password(self, raw_passwrod: str) -> None:
        self.password = generate_hashed_password(raw_passwrod)
        
    def check_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)
    
    @staticmethod
    def make_passsword(raw_password: str) -> str:
        return generate_hashed_password(raw_password)