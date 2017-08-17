import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)

    password = Column(String)
    mobile = Column(String)
    email = Column(String)
    isApproved = Column(Integer)

engine = create_engine('sqlite:///kslbackend.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

def getUsers():
    session = DBSession()
    return session.query(User).all()


def saveUser(user):
    session = DBSession()
    session.add(user)
    session.commit()

