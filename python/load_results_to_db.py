# load_places_to_db.py
# This file is part of the Ptolemy Layer for Google Earth project.
# It loads our data into the database.

import os
import sys
import argparse

import common

import numpy as np
import psycopg2
from geoalchemy2.shape import from_shape
import models
from shapely.geometry import Point
import pandas as pd

def main(places):
    valid_dispositions = ('known', 'unknown', 'tentative')
    try:
        #connection = psycopg2.connect("dbname='ptolemy' user='ptolemy' host='localhost' password='ptolemy' port='5433'")
        session = models.create_session()
        print 'connected'
        #cursor = connection.cursor()
        #cursor.execute('''DELETE FROM places''')
        #query = '''INSERT INTO places (ptolemy_id, ptolemy_name, modern_name, ptolemy_point, modern_point, disposition) VALUES (%s, %s, %s, ST_GeogFromText(%s), ST_GeogFromText(%s), %s)'''
        for index, row in places.iterrows():
            print index
            try:
                place = session.query(models.Place).get(row.ptol_id)
                if place == None:
                    print 'inserting %s' % (row.ptol_id)
                    place = models.Place()
                    place.ptolemy_id = row.ptol_id
                else:
                    print 'updating %s' % (row.ptol_id)

                place.ptolemy_name = row.ptol_name
                if isinstance(row.modern_name, basestring):
                    place.modern_name = row.modern_name
                else:
                    place.modern_name = None
                place.ptolemy_point = from_shape(Point(row.ptol_lon, row.ptol_lat))
                if np.isnan(row.modern_lat) or np.isnan(row.modern_lon):
                    place.modern_point = None
                else:
                    place.modern_point = from_shape(Point(row.modern_lon, row.modern_lat))
                if row.disposition not in valid_dispositions:
                    place.disposition = None
                else:
                    place.disposition = row.disposition

                session.add(place)

                #cursor.execute(query, place_data)
            except Exception as e:
                print 'unable to insert %s: %s' % (row.ptol_id, e.message)
        #connection.commit()
        #cursor.close()
        #connection.close()
        session.commit()
        session.close()
    except Exception as e:
        print 'unable to connect: %s' % (e.message, )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Load Ptolemy places to database.')
    parser.add_argument('--sgdb', help='read from sgdb with given prefix')
    parser.add_argument('--xlsx', help='xlsx to read from instead of sgdb')

    args = parser.parse_args()

    if args.sgdb:
        places = common.read_places(args.sgdb)
    elif args.xlsx:
        places = common.read_places_xlsx(args.xlsx)
    else:
        sys.stderr.write('must specify one of --sgdb or --xlsx')
        exit(1)

    places = common.read_places_output_csv(args.csv)

    #main(places)
