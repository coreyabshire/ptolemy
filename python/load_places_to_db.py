# load_places_to_db.py
# This file is part of the Ptolemy Layer for Google Earth project.
# It loads our data into the database.

import os
import sys
import argparse

import common

import numpy as np
import psycopg2

def main(places):
    valid_dispositions = ('known', 'unknown', 'tentative')
    try:
        connection = psycopg2.connect("dbname='ptolemy' user='ptolemy' host='localhost' password='ptolemy' port='5433'")
        print 'connected'
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM places''')
        query = '''INSERT INTO places (ptolemy_id, ptolemy_name, modern_name, ptolemy_point, modern_point, disposition) VALUES (%s, %s, %s, ST_GeogFromText(%s), ST_GeogFromText(%s), %s)'''
        for index, place in places.iterrows():
            try:
                point_data = (place.ptol_lon, place.ptol_lat, place.modern_lon, place.modern_lat)
                if any(np.isnan(x) for x in point_data):
                    print 'not inserting: %s contains null point data %s' % (place.ptol_id, point_data)
                elif place.disposition not in valid_dispositions:
                    print 'not inserting: %s has invalid disposition %s' % (place.ptol_id, place.disposition)
                else:
                    place_data = (
                        place.ptol_id,
                        place.ptol_name,
                        place.modern_name,
                        'POINT(%f %f)' % (place.ptol_lon, place.ptol_lat),
                        'POINT(%f %f)' % (place.modern_lon, place.modern_lat),
                        place.disposition)
                    print 'inserting %s: %s' % (place.ptol_id, place_data)
                    cursor.execute(query, place_data)
            except Exception as e:
                print 'unable to insert %s: %s' % (place.ptol_id, e.message)
        connection.commit()
        cursor.close()
        connection.close()
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

    main(places)
