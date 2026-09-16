from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Column, String
from main import engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)

Base.metadata.create_all(engine)