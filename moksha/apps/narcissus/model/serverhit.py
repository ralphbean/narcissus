import datetime

from sqlalchemy import Column
from sqlalchemy import Integer, String, Float, DateTime

from moksha.apps.narcissus.model import DeclarativeBase

class ServerHit(DeclarativeBase):
    """ Represents a single log entry """
    __tablename__ = 'iplatlon'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=datetime.datetime.now)
    ip = Column(String(40))
    lat = Column(Float)
    lon = Column(Float)
    mag = Column(Float)
