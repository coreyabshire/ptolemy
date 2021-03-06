# regression_measure.py: Predict modern coordinates for places
# described by Ptolemy using linear regression against
# the places that have been suggested by other means.

import os
import logging

import pandas as pd
from sklearn import linear_model
from sklearn.cross_validation import LeaveOneOut
from geopy.distance import vincenty

import sgdb
import geocode

PTOL_HOME = os.environ['PTOL_HOME']
logging.basicConfig(level='DEBUG')

KEY_PLACE_FIELDNAMES = [
    'ptol_id',
    'ptol_name',
    'ptol_lat',
    'ptol_lon',
    'modern_name']

X_NAMES = [
    'ptol_lat',
    'ptol_lon']

# book 7 contains India
# chapter 1 is within the Ganges
TARGET_BOOK = '7.01' 

places = sgdb.read_places().drop_duplicates('ptol_id')
places.reindex(columns=['ptol_id'])
places = places.loc[pd.notnull(places.ptol_lat), :]
places = places.loc[:, KEY_PLACE_FIELDNAMES]
places = places.loc[places.ptol_id.str.startswith(TARGET_BOOK), :]
places = pd.merge(places, geocode.read_geocodes(), how='left')
known = places.loc[pd.notnull(places.modern_lat), :]
known.is_copy = False
known.to_csv('../Data/regression_measure_before.csv', encoding='cp1252')

loo = LeaveOneOut(len(known))
for train, test in loo:
    trainx = known.iloc[train, :].loc[:, X_NAMES]
    testx = known.iloc[test, :].loc[:, X_NAMES]
    lonreg = linear_model.LinearRegression()
    latreg = linear_model.LinearRegression()
    lonreg.fit(trainx, known.iloc[train, :].modern_lon)
    latreg.fit(trainx, known.iloc[train, :].modern_lat)
    known.loc[known.iloc[test, :].index, 'pred_lat'] = latreg.predict(testx)
    known.loc[known.iloc[test, :].index, 'pred_lon'] = lonreg.predict(testx)

for i, p in known.iterrows():
    lat_err = p.modern_lat - p.pred_lat
    lon_err = p.modern_lon - p.pred_lon
    sq_err = lat_err ** 2 + lon_err ** 2
    modern_coords = (p.modern_lat, p.modern_lon)
    pred_coords = (p.pred_lat, p.pred_lon)
    dist_err = vincenty(modern_coords, pred_coords).miles
    known.loc[i, 'lat_err'] = lat_err
    known.loc[i, 'lon_err'] = lon_err
    known.loc[i, 'sq_err'] = sq_err
    known.loc[i, 'dist_err'] = dist_err

known.to_csv('../Data/regression_measure.csv', encoding='cp1252')
