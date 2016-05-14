#!/usr/bin/python

import psycopg2
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response, send_file
from contextlib import closing
import logging
from logging.handlers import RotatingFileHandler
from geoalchemy2.shape import from_shape, to_shape
import models
import StringIO
import unicodecsv
from shapely.geometry import Point

from app import app
from app import main

if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run()
