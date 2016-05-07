from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geography
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from shapely import wkb
import geoalchemy2.functions
from geoalchemy2.shape import to_shape


DB_URL = 'postgresql://ptolemy:ptolemy@localhost:5433/ptolemy'

Base = declarative_base()

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

def main():
    engine = create_engine(DB_URL, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    for place in session.query(Place).order_by(Place.ptolemy_name):
        #point = wkb.loads(place.ptolemy_point)
        point = to_shape(place.ptolemy_point)
        print place.ptolemy_id, place.ptolemy_name, point.x, point.y
    session.close()

if __name__ == '__main__':
    main()