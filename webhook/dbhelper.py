
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'

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

def getAccounts():
    session = DBSession()
    return session.query(Account).all()


def saveAccount(account):
    session = DBSession()
    session.add(account)
    session.commit()

