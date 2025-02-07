from sqlalchemy import (
    Boolean,
    Column, 
    Enum,   
    Integer, 
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship
from simple_crud_api.database import Base

from ..utils.security.passwd import generate_hashed_password, check_password
from ..utils.user import UserType

class Validation(Base):
    __tablename__ = "validation"
    
    id = Column(String(36), primary_key=True)
    active = Column(Boolean, default=True)
    
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    user = relationship("User", back_populates="validation")
    
    @property
    def get_status(self):
        return self.active
    
    @property
    def get_validation_id(self):
        return self.id
    
    @property
    def get_user_id(self):
        return self.user_id