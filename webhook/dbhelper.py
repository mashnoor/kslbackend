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


# engine = create_engine('sqlite:///kslbackend.db')

class DBManager:

    def __init__(self):

        engine = create_engine(
            'mysql+pymysql://' + settings.db_user + ':' + settings.db_pass + '@localhost/ksl?host=localhost?port=3306')
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        self.DBSession = sessionmaker(bind=engine)

    def getMasterAccounts(self):
        session = self.DBSession()
        result = session.query(Account).all()
        session.close()
        return result

    def getRequisitions(self):
        session = self.DBSession()
        result = session.query(FundRequisition).all()
        session.close()
        return result

    def getAccountRequests(self):
        session = self.DBSession()
        result = session.query(AccountRequest).all()
        session.close()
        return result

    def getAccounts(self):
        session = self.DBSession()
        result = session.query(Account).all()
        return result

    def getItsAccounts(self, masterId):
        session = self.DBSession()
        result = session.query(Account).filter_by(masterId=masterId).first().itsaccounts
        session.close()
        return result

    def getItsAccountsMobile(self, masterId, masterPass):
        session = self.DBSession()
        result = session.query(Account).filter_by(masterId=masterId, masterPassword=masterPass).first().itsaccounts
        session.close()
        return result

    def addItsAccoount(self, masterid, itsaccount):
        session = self.DBSession()
        account = session.query(Account).filter_by(masterId=masterid).first()
        account.itsaccounts.append(itsaccount)
        session.commit()
        session.close()

    def setToken(self, masterid, token):
        session = self.DBSession()
        account = session.query(Account).filter_by(masterId=masterid).first()
        account.token = token
        session.commit()
        session.close()

    def getToken(self, masterid):
        session = self.DBSession()
        account = session.query(Account).filter_by(masterId=masterid).first()
        result = account.token
        session.close()
        return result

    def addNotification(self, masterid, notification):
        session = self.DBSession()
        account = session.query(Account).filter_by(masterId=masterid).first()
        account.notifications.append(notification)
        session.commit()
        session.close()

    def addGroupNotification(self, masterids, notification):
        session = self.DBSession()
        for masterid in masterids:
            account = session.query(Account).filter_by(masterId=masterid).first()
            account.notifications.append(notification)
        session.commit()
        session.close()

    def save(self, data):
        session = self.DBSession()
        session.add(data)
        session.commit()
        session.close()

    def isValiedMasterId(self, masterid, masterpassword):
        session = self.DBSession()
        result = session.query(Account).filter_by(masterId=masterid, masterPassword=masterpassword).scalar() is not None
        session.close()
        return result

    def getMasterAccount(self, masterid, masterpassword):
        session = self.DBSession()
        result = session.query(Account).filter_by(masterId=masterid, masterPassword=masterpassword).first()
        session.close()
        return result

    def getNotifications(self, masterid):
        session = self.DBSession()
        account = session.query(Account).filter_by(masterId=masterid).first()
        result = account.notifications
        session.close()
        return result

    def getClientIdsMobile(self, masterId, masterPass):
        session = self.DBSession()
        result = session.query(Account).filter_by(masterId=masterId, masterPassword=masterPass).first().clientids
        session.close()
        return result

    def getClientIds(self, masterId):
        session = self.DBSession()
        result =  session.query(Account).filter_by(masterId=masterId).first().clientids
        session.close()
        return result

    def addClientId(self, masterid, clientid):
        session = self.DBSession()
        account = session.query(Account).filter_by(masterId=masterid).first()
        account.clientids.append(clientid)
        session.commit()
        print(clientid.clientidno)
        session.close()

    def deleteItsId(self, masterid, itsid):
        session = self.DBSession()
        for itsacc in session.query(Account).filter_by(masterId=masterid).first().itsaccounts:
            if itsacc.itsNo == itsid:
                # account = session.query(Account).filter_by(masterId=masterid).first()
                session.delete(itsacc)
                session.commit()
                print("Deleted")
        session.close()

    def updateItsId(self, masterid, itsid, itsNewPass):
        session = self.DBSession()
        for itsacc in session.query(Account).filter_by(masterId=masterid).first().itsaccounts:
            if itsacc.itsNo == itsid:
                # account = session.query(Account).filter_by(masterId=masterid).first()
                itsacc.password = itsNewPass
                session.commit()
                session.close()
                return 'success'
        session.close()
        return 'failed'

    def getMasterPassword(self, email, masterId):
        session = self.DBSession()
        result = session.query(Account).filter_by(email=email, masterId=masterId).first().masterPassword
        session.close()
        return result


