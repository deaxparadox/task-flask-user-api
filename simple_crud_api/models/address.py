from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Address(Base):
    __tablename__ = "address"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    line1 = Column(String(50))
    line2 = Column(String(50), nullable=True)
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    pincode = Column(String(50), nullable=True)
    
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    user = relationship("User", back_populates="address")
    
    def get_reqired_fields(self):
        fields = self.get_fields()
        for x in ['id', 'user_id', 'line2']:
            fields.remove(x)
        return fields
    
    def get_optional_fields(self):
        return ['line2']
    
    def get_fields(self):
        return [c.name for c in self.__table__.columns]
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}