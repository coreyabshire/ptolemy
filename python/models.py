from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geography
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DB_URL = 'postgresql://ptolemy:ptolemy@localhost:5433/ptolemy'


def create_session():
    engine = create_engine(DB_URL, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class Place(Base):
    __tablename__ = 'places'

    ptolemy_id = Column(String, primary_key=True)
    ptolemy_name = Column(String)
    modern_name = Column(String)
    ptolemy_point = Column(Geography(geometry_type='POINT'))
    modern_point = Column(Geography(geometry_type='POINT'))
    disposition = Column(String)

    def __repr__(self):
        return '<Place(%s)>' % (self.ptolemy_id, )

