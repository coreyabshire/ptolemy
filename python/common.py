# common.py
# Contains the common configuration constants and function definitions
# for the various place estimation modules we are trying for the Ptolemy
# project.

import os
import logging

import pandas as pd
import numpy as np

import sgdb
import geocode

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

PTOL_HOME = os.environ['PTOL_HOME']
logging.basicConfig(level='DEBUG')

KEY_PLACE_FIELDNAMES = [
    'ptol_id',
    'ptol_name',
    'ptol_lat',
    'ptol_lon',
    'modern_name']

# book 7 contains India
# chapter 1 is within the Ganges
# chapter 4 is Sri Lanka (mostly)
TARGET_BOOK = '7.01'


def construct_model(modelname):
    mname = modelname.lower()
    cname = modelname.capitalize()
    return getattr(__import__(mname, cname), cname)()


def read_places(id_starts_with):
    """Read places for this script."""
    places = sgdb.read_places()
    places = places.loc[pd.notnull(places.ptol_lat), :]
    places = places.drop_duplicates('ptol_id')
    places = places.loc[:, KEY_PLACE_FIELDNAMES]
    places = places.loc[places.ptol_id.str.startswith(id_starts_with), :]
    print len(places.ptol_id)
    places = pd.merge(places, geocode.read_geocodes(), how='left')
    places.loc[pd.notnull(places.modern_lat), 'disposition'] = 'known'
    places.loc[pd.isnull(places.modern_lat), 'disposition'] = 'unknown'
    places.set_index('ptol_id', False, False, True, True)
    print len(places.ptol_id)
    return places


def read_places_xlsx(filename):
    """Read a set of places from an Excel spreadsheet, formatted
    the way we've adopted during this project."""
    places = pd.read_excel(filename, 0, encoding='utf-8')
    places = places.iloc[:, 0:8]
    places.columns = ['ptol_id', 'ptol_name', 'modern_name',
                      'ptol_lat', 'ptol_lon', 'modern_lat', 'modern_lon',
                      'disposition']
    places = places.drop_duplicates('ptol_id')
    places.set_index('ptol_id', False, False, True, True)
    return places


def read_places_output_csv(filename):
    """Read a set of places from the CSV the predictors write out
    the way we've adopted during this project."""
    places = pd.read_csv(filename, encoding="ISO-8859-1")
    places = places.iloc[:, 0:8]
    places.columns = ['ptol_id', 'ptol_name', 'modern_name', 'disposition',
                      'ptol_lat', 'ptol_lon', 'modern_lat', 'modern_lon']
    places = places.drop_duplicates('ptol_id')
    places.set_index('ptol_id', False, False, True, True)
    return places


def split_places(places):
    """Split places into known and unknown places."""
    known = places.loc[places.disposition == 'known', :]
    unknown = places.loc[places.disposition != 'known', :]
    # prevent warning below that it's a copy of places
    known.is_copy = False
    unknown.is_copy = False 
    return known, unknown


def report_places(places):
    """A debugging function to report lat/lon pairs for each place."""
    print places.loc[:, ['ptol_lat','ptol_lon']]


def report_simplices(tri, points):
    """A debugging function to report the triangulation computed."""
    print tri.simplices
    for s in tri.simplices:
        print [(lat, lon) for (lat, lon) in [points.ix[p] for p in s]]


def write_points(kml, places, name_col, lon_col, lat_col, color):
    """Write a series of placemarks into kml from places, using the name,
    lon and lat columns specified by the corresponding col parameters, and
    using the specified color."""
    for i, r in places.iterrows():
        placemark_id = 'placemark_%s' % r[name_col]
        point_id = 'point_%s' % r[name_col]
        kml.write('''
        <Placemark id="%s">
            <name>%s</name>
            <styleUrl>#%s_point</styleUrl>
            <Point id="%s">
                <coordinates>%s,%s,0.0</coordinates>
            </Point>
        </Placemark>
''' % (placemark_id, r[name_col], color, point_id, r[lon_col], r[lat_col]))


def write_line(kml, a, b, color):
    """Write a line for each simplex in tri, each of which refers to
    a point in places by index, using the lat, lon columns specified and
    in the specified color."""
    kml.write('''
        <Placemark>
            <name></name>
            <styleUrl>#%s_line</styleUrl>
            <LineString>
                <extrude>0</extrude>
                <tessellate>1</tessellate>
                <altitudeMode>clampToGround</altitudeMode>
                <coordinates>
                     %f,%f,0
                     %f,%f,0
                </coordinates>
            </LineString>
        </Placemark>\n''' % (color, a[1], a[0], b[1], b[0]))


def write_point(kml, color, p, label=''):
    kml.write('''
        <Placemark>
            <name>%s</name>
            <styleUrl>#%s_point</styleUrl>
            <Point>
                <coordinates>%s,%s,0.0</coordinates>
            </Point>
        </Placemark>''' % (label, color, p[1], p[0]))


def write_three_lines(kml, places, source_prefix, dest_suffix, color):
    source_lon_col = source_prefix + '_lon'
    source_lat_col = source_prefix + '_lat'
    prefixes = ['a','b','c']
    dest_lon_cols = ['%s%s_lon' % (pre, dest_suffix) for pre in prefixes]
    dest_lat_cols = ['%s%s_lat' % (pre, dest_suffix) for pre in prefixes]
    for i, p in places.iterrows():
        source_lon = p[source_lon_col]
        source_lat = p[source_lat_col]
        for j in range(len(prefixes)):
            dest_lon = p[dest_lon_cols[j]]
            dest_lat = p[dest_lat_cols[j]]
            coords = [(source_lon,source_lat), (dest_lon,dest_lat)]
            write_line(kml, coords, color)


def write_csv_file(filename, known, unknown):
    """Write out a csv file to filename containing all places listed in
    known and unknown. Those to dataframes are merged and sorted by ptol_id
    prior to being written."""
    places = unknown.append(known, True, False)
    places.sort_values('ptol_id', inplace=True)
    cols = [
        'ptol_id',
        'ptol_name',
        'modern_name',
        'disposition',
        'ptol_lat',
        'ptol_lon',
        'modern_lat',
        'modern_lon']
    if 'original_lat' in unknown.columns:
        cols += ['original_lat', 'original_lon']
    places.to_csv(filename, index=False, encoding='utf-8', columns=cols)


def write_map_file(filename, known, unknown, width, height, dpi, labels_col, title):
    data = unknown.append(known, True, False)
    enlarge_by = 0.1
    plt.figure(num=None, figsize=(width, height), dpi=dpi,
               facecolor='w', edgecolor='k')
    data = data.loc[data.modern_lat != 0.0, :]
    ll = data.modern_lat.min(), data.modern_lon.min(),
    ur = data.modern_lat.max(), data.modern_lon.max(),
    adj = tuple((ur[i] - ll[i]) * enlarge_by for i in range(2))
    ll = tuple(ll[i] - adj[i] for i in range(2))
    ur = tuple(ur[i] + adj[i] for i in range(2))
    lat0 = ll[0] + ((ur[0] - ll[0]) / 2.0)
    lon0 = ll[1] + ((ur[1] - ll[1]) / 2.0)
    bmap = Basemap(projection='merc', resolution='l',
                   lon_0=lon0,
                   lat_0=90.0, lat_ts=lat0,
                   llcrnrlat=ll[0],
                   llcrnrlon=ll[1],
                   urcrnrlat=ur[0],
                   urcrnrlon=ur[1])
    bmap.shadedrelief()
    bmap.drawmapboundary()
    bmap.drawmeridians(np.arange(0, 360, 5), labels=[0, 0, 0, 1], fontsize=10)
    bmap.drawparallels(np.arange(-90, 90, 5), labels=[1, 0, 0, 0], fontsize=10)
    bmap.drawcounties(linewidth=1)
    for disp, col in [('known', 'c'), ('unknown', 'm'), ('tentative', 'b')]:
        i = data.disposition == disp
        lats = [lat for lat in list(data.loc[i, 'modern_lat']) if lat != 0.0]
        lons = [lon for lon in list(data.loc[i, 'modern_lon']) if lon != 0.0]
        x, y = bmap(lons, lats)
        bmap.scatter(x, y, 8, marker='o', color=col, label=disp)
        if filename:
            labels = []
            for s in data.loc[i, labels_col]:
                labels.append(s if type(s) == unicode else u'')
            for label, xi, yi in zip(labels, x, y):
                plt.text(xi, yi, label)
    plt.title(title)
    plt.legend()
    if filename:
        plt.savefig(filename, dpi=dpi)
    else:
        plt.show()


def write_point_style(kml, color_name, color_code):
    kml.write('''
        <Style id="%s_point">
            <IconStyle id="substyle_0">
                <color>%s</color>
                <colorMode>normal</colorMode>
                <scale>1</scale>
                <heading>0</heading>
                <Icon id="link_0">
                    <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
                </Icon>
            </IconStyle>
        </Style>\n''' % (color_name, color_code))


def write_line_style(kml, color_name, color_code):
    kml.write('''
        <Style id="%s_line">
            <LineStyle id="substyle_120">
                <color>%s</color>
                <colorMode>normal</colorMode>
                <width>2</width>
            </LineStyle>
        </Style>\n'''  % (color_name, color_code))


def write_styles(kml, a='ff'):
    colors = [('red',    a+'0000ff'),
              ('orange', a+'0099ff'),
              ('yellow', a+'00ffff'),
              ('green',  a+'00ff00'),
              ('cyan',   a+'ffff00'),
              ('purple', a+'ff00ff')]
    for name, code in colors:
        write_point_style(kml, name, code)
        write_line_style(kml, name, code)


def write_kml_file(filename, tri, known, unknown):
    """Write the KML file for the triangulation."""
    with open(filename, 'w') as kml:
        kml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        kml.write('<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">\n')
        kml.write('<Document id="ptolemy-7.01">\n')
        write_styles(kml)
        write_points(kml, known, 'ptol_id', 'ptol_lon', 'ptol_lat', 'yellow')
        write_points(kml, known, 'ptol_id', 'modern_lon', 'modern_lat', 'yellow')
        write_points(kml, unknown, 'ptol_id', 'ptol_lon', 'ptol_lat', 'red')
        write_points(kml, unknown, 'ptol_id', 'modern_lon', 'modern_lat', 'red')
        kml.write('</Document>\n')
        kml.write('</kml>\n')

