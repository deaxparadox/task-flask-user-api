from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from . import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
db_session = scoped_session(
    sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=engine
        )
    )

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from .models import user, vendor
    
    Base.metadata.create_all(bind=engine)
    