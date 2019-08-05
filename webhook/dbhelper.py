from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
import settings

Base = declarative_base()


class AccountRequest(Base):
    __tablename__ = 'accountrequests'

    id = Column(Integer, primary_key=True)
    name = Column(String(500))

    password = Column(String(500))
    mobile = Column(String(500))
    email = Column(String(500))
    details = Column(String(500))


class FundRequisition(Base):
    __tablename__ = 'requisitions'
    id = Column(Integer, primary_key=True)
    itsaccno = Column(String(500))
    amount = Column(String(500))
    reqdate = Column(String(500))
    isApproved = Column(Integer)


class Account(Base):
    __tablename__ = 'accounts'

    masterId = Column(String(500), primary_key=True)

    masterPassword = Column(String(500))
    name = Column(String(500))
    detail = Column(String(500))
    token = Column(String(500))
    email = Column(String(500))
    itsaccounts = relationship('ITSAccount', backref="accounts")
    notifications = relationship('Notification', backref="accounts")
    clientids = relationship('Clientid', backref="accounts")


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    message = Column(String(500))
    sendTimestamp = Column(DateTime)

    accountId = Column(String(500), ForeignKey("accounts.masterId"))


class ITSAccount(Base):
    __tablename__ = 'itsaccounts'

    id = Column(Integer, primary_key=True)
    itsNo = Column(String(500))
    password = Column(String(500))
    accountId = Column(String(500), ForeignKey('accounts.masterId'))


class Clientid(Base):
    __tablename__ = 'clientids'

    id = Column(Integer, primary_key=True)
    clientidno = Column(String(500))
    accountId = Column(String(500), ForeignKey('accounts.masterId'))


#engine = create_engine('sqlite:///kslbackend.db')
engine = create_engine('mysql+pymysql://' + settings.db_user +':' + settings.db_pass +'@localhost/ksl?host=localhost?port=3306')
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


def updateItsId(masterid, itsid, itsNewPass):
    session = DBSession()
    for itsacc in session.query(Account).filter_by(masterId=masterid).first().itsaccounts:
        if itsacc.itsNo == itsid:
            # account = session.query(Account).filter_by(masterId=masterid).first()
            itsacc.password = itsNewPass
            session.commit()
            return 'success'
    return 'failed'


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
