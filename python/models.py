from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geography
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

#DB_URL = 'postgresql://claudiusptolemy:cbMI2Sy41KUyOO42jkLN@localhost:5435/claudiusptolemy'
DB_URL = 'postgresql://claudiusptolemy:changeme@localhost:5433/claudiusptolemy'

def create_session(dburl):
    engine = create_engine(dburl, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)

    def __repr__(self):
        return '<Project(%s,%s)>' % (self.id, self.name)

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)

    def __repr__(self):
        return '<Region(%s,%s)>' % (self.id, self.name)

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

