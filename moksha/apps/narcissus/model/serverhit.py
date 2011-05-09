import datetime

from sqlalchemy import Column
from sqlalchemy import Integer, String, Float, DateTime

from moksha.apps.narcissus.model import DeclarativeBase

class ServerHit(DeclarativeBase):
    """ Represents a single log entry """
    __tablename__ = 'iplatlon'

    id = Column(Integer, primary_key=True)
    insdatetime = Column(DateTime, default=datetime.datetime.now)
    ip = Column(String(40))
    lat = Column(Float)
    lon = Column(Float)
    logdatetime = Column(DateTime, default=datetime.datetime.now)
    filesize = Column(Float)
    bytesin = Column(Float)
    bytesout = Column(Float)
    statuscode = Column(Float)
    refererhash = Column(String(32))
    filenamehash = Column(String(32))
    requesttype = Column(String(10))
    httptype = Column(String(10))
