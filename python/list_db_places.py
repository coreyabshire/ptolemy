from shapely import wkb
import geoalchemy2.functions
from geoalchemy2.shape import to_shape

from models import Place, create_session


def main():
    session = create_session()
    for place in session.query(Place).order_by(Place.ptolemy_name):
        #point = wkb.loads(place.ptolemy_point)
        point = to_shape(place.ptolemy_point)
        print place.ptolemy_id, place.ptolemy_name, point.x, point.y
    session.close()

if __name__ == '__main__':
    main()