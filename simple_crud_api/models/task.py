from enum import Enum

from sqlalchemy import (
    Column, 
    Integer, 
    String,
    Enum as SQLEnum,
    ForeignKey
)
from sqlalchemy.orm import relationship

from ..database import Base


class TaskStatus(Enum):
    NotStarted = 'not-started'
    Inprogress = 'in-progress'
    Completed = 'completed'
    PendingReview = 'pending-review'
    Done = 'done'


class Task(Base):
    __tablename__ = 'task'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(200))
    body = Column(String(2000))
    
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.NotStarted)
    
    # Team leand or Manager
    created_by_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    assigned_by_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    # Employee
    assigned_to_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    
    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="task_created_by")
    assigned_by = relationship("User", foreign_keys=[assigned_by_id], back_populates="task_assigned_by")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id], back_populates="task_received")
    
    def get_fields(self):
        return [c.name for c in self.__table__.columns]
    
    def get_response_fields(self):
        all_fields = self.get_fields()
        # for x in ["assigned_by_manager_id", "assigned_by_team_lead_id", "assigned_to_id"]:
        #     all_fields.remove(x)
        return all_fields
    
    def to_dict(self):
        data = {}
        for c in self.get_response_fields():
            if c == "status":
                data.update({c: getattr(self, c).value})
            else:
                data.update({c: getattr(self, c)})
        return  data