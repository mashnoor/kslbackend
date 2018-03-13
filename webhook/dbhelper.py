from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class AccountRequest(Base):
    __tablename__ = 'accountrequests'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    password = Column(String)
    mobile = Column(String)
    email = Column(String)
    details = Column(String)


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
    token = Column(String)
    email = Column(String)
    itsaccounts = relationship('ITSAccount', backref="accounts")
    notifications = relationship('Notification', backref="accounts")
    clientids = relationship('Clientid', backref="accounts")


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    message = Column(String)
    sendTimestamp = Column(DateTime)

    accountId = Column(String, ForeignKey("accounts.masterId"))


class ITSAccount(Base):
    __tablename__ = 'itsaccounts'

    id = Column(Integer, primary_key=True)
    itsNo = Column(String)
    password = Column(String)
    accountId = Column(String, ForeignKey('accounts.masterId'))


class Clientid(Base):
    __tablename__ = 'clientids'

    id = Column(Integer, primary_key=True)
    clientidno = Column(String)
    accountId = Column(String, ForeignKey('accounts.masterId'))


engine = create_engine('sqlite:///kslbackend.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def getMasterAccounts():
    session = DBSession()
    return session.query(Account).all()


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


def getItsAccountsMobile(masterId, masterPass):
    session = DBSession()
    return session.query(Account).filter_by(masterId=masterId, masterPassword=masterPass).first().itsaccounts


def addItsAccoount(masterid, itsaccount):
    session = DBSession()
    account = session.query(Account).filter_by(masterId=masterid).first()
    account.itsaccounts.append(itsaccount)
    session.commit()


def setToken(masterid, token):
    session = DBSession()
    account = session.query(Account).filter_by(masterId=masterid).first()
    account.token = token
    session.commit()


def getToken(masterid):
    session = DBSession()
    account = session.query(Account).filter_by(masterId=masterid).first()
    return account.token


def addNotification(masterid, notification):
    session = DBSession()
    account = session.query(Account).filter_by(masterId=masterid).first()
    account.notifications.append(notification)
    session.commit()


def addGroupNotification(masterids, notification):
    session = DBSession()
    for masterid in masterids:
        account = session.query(Account).filter_by(masterId=masterid).first()
        account.notifications.append(notification)
    session.commit()


def save(data):
    session = DBSession()
    session.add(data)
    session.commit()


def isValiedMasterId(masterid, masterpassword):
    session = DBSession()
    return session.query(Account).filter_by(masterId=masterid, masterPassword=masterpassword).scalar() is not None

def getMasterAccount(masterid, masterpassword):
    session = DBSession()
    return session.query(Account).filter_by(masterId=masterid, masterPassword=masterpassword).first()

def getNotifications(masterid):
    session = DBSession()
    account = session.query(Account).filter_by(masterId=masterid).first()
    return account.notifications


def getClientIdsMobile(masterId, masterPass):
    session = DBSession()
    return session.query(Account).filter_by(masterId=masterId, masterPassword=masterPass).first().clientids


def getClientIds(masterId):
    session = DBSession()
    return session.query(Account).filter_by(masterId=masterId).first().clientids


def addClientId(masterid, clientid):
    session = DBSession()
    account = session.query(Account).filter_by(masterId=masterid).first()
    account.clientids.append(clientid)
    session.commit()
    print(clientid.clientidno)


def deleteItsId(masterid, itsid):
    session = DBSession()
    for itsacc in session.query(Account).filter_by(masterId=masterid).first().itsaccounts:
        if itsacc.itsNo == itsid:
            # account = session.query(Account).filter_by(masterId=masterid).first()
            session.delete(itsacc)
            session.commit()
            print("Deleted")


def getMasterPassword(email, masterId):
    session = DBSession()
    return session.query(Account).filter_by(email=email, masterId=masterId).first().masterPassword


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

