# -*- coding: utf-8 -*-
"""The `model` is more generally speaking a set of python objects mapped to
a database through the `SQLAlchemy <http://sqlalchemy.org>`_ module.

Database objects loaded as SQLA objects (as `model` objects) cache any
modifications made to them and only write them to the database as a whole
at the end of the request (if and only if the request terminates successfully).

The advantages here three-fold:
 - Database changes are only written (`committed`) to the database once no
   errors were known to have occurred during the request.
 - Database update and select statements can be optimized and combined to
   reduce general DB overhead.
 - Programming is made more comfortable by working with familiar objects than
   with terse and often cumbersome SQL statements.

"""

from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# Global session manager: DBSession() returns the Thread-local
# session object appropriate for the current web request.
maker = sessionmaker(autoflush=False, autocommit=False)
DBSession = scoped_session(maker)

# Base class for all of our model classes: By default, the data model is
# defined with SQLAlchemy's declarative extension, but if you need more
# control, you can switch to the traditional method.
DeclarativeBase = declarative_base()

# There are two convenient ways for you to spare some typing.
# You can have a query property on all your model classes by doing this:
DeclarativeBase.query = DBSession.query_property()
# Or you can use a session-aware mapper as it was used in TurboGears 1:
# DeclarativeBase = declarative_base(mapper=DBSession.mapper)

# Global metadata.
# The default metadata is the one from the declarative base.
metadata = DeclarativeBase.metadata

# If you have multiple databases with overlapping table names, you'll need a
# metadata for each database. Feel free to rename 'metadata2'.
#metadata2 = MetaData()

def init_model(engine):
    # This gets called later by the TG2.1 startup process
    DBSession.configure(bind=engine)

# Import your model modules here.
from narcissus.model.serverhit import ServerHit
from narcissus.model.auth import User, Group, Permission

__all__ = [ServerHit, User, Group, Permission]
