import sys, string, GeoIP, time, datetime
gi = GeoIP.open("/usr/share/GeoIP/GeoLiteCity.dat", GeoIP.GEOIP_MEMORY_CACHE)

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String, Float, DateTime

engine = create_engine(
    'mysql://mirrorip:HBqUPx4yxhWdtrQG@washington.rit.edu/mirrorip',
    echo=True)
metadata = MetaData(bind=engine)

iplatlon_table = Table('iplatlon', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('datetime', DateTime,default=datetime.datetime.now),
                    Column('ip', String(40)),
                    Column('lat', Float),
                    Column('lon', Float),
                    Column('mag', Float),
                    )

# create tables in database
metadata.create_all()

# create a database connection
conn = engine.connect()

