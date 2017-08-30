from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class AccountRequest(Base):
    __tablename__ = 'accountrequests'

    id = Column(Integer, primary_key=True)
    username = Column(String)

    password = Column(String)
    mobile = Column(String)
    email = Column(String)
    isApproved = Column(Integer)


class FundRequisition(Base):

    __tablename__ = 'requisitions'
    id = Column(Integer, primary_key=True)
    itsaccno = Column(String)
    amount = Column(String)
    reqdate = Column(String)
    isApproved = Column(Integer)


class Account(Base):
    __tablename__ = 'accounts'


    masterId = Column(String, primary_key=True)

    masterPassword = Column(String)
    name = Column(String)
    detail = Column(String)
    itsaccounts = relationship('ITSAccount', backref="accounts")

class ITSAccount(Base):
    __tablename__ = 'itsaccounts'

    id = Column(Integer, primary_key=True)
    itsNo = Column(String)
    password = Column(String)
    accountId = Column(String, ForeignKey('accounts.masterId'))

engine = create_engine('sqlite:///kslbackend.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

def getRequisitions():
    session = DBSession()
    return session.query(FundRequisition).all()


def getAccountRequests():
    session = DBSession()
    return session.query(AccountRequest).all()

def getAccounts():
    session = DBSession()
    return session.query(Account).all()

def getItsAccounts(masterId):
    session = DBSession()
    return session.query(Account).filter_by(masterId=masterId).first().itsaccounts

def addItsAccoount(masterid, itsaccount):
    session = DBSession()
    account = session.query(Account).filter_by(masterId=masterid).first()
    account.itsaccounts.append(itsaccount)
    session.commit()

'''
def saveRequisitionRequest(requisition):
    session = DBSession()
    session.add(requisition)
    session.commit()


def saveAccount(account):
    session = DBSession()
    session.add(account)
    session.commit()

'''
def save(data):
    session = DBSession()
    session.add(data)
    session.commit()

'''
itsacc = ITSAccount()
itsacc.password = "1111"
itsacc.itsNo = "13423"


acc = Account()
acc.masterId = "8888"
acc.detail = "This is a account"
acc.name = "Name"
acc.masterPassword = "00000"
acc.itsaccounts.append(itsacc)

saveAccount(acc)

'''
