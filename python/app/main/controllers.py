import psycopg2
from flask import Blueprint, Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response, send_file
from contextlib import closing
import logging
from logging.handlers import RotatingFileHandler
from geoalchemy2.shape import from_shape, to_shape
import models
import forms
import StringIO
import unicodecsv
from shapely.geometry import Point
from flask import current_app

main = Blueprint('main', __name__)

def connect_db():
    #return sqlite3.connect(app.config['DATABASE'])
    return psycopg2.connect("dbname='claudiusptolemy' user='claudiusptolemy' host='localhost' password='changeme' port='5432'")


def init_db():
    with closing(connect_db()) as db:
        with main.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@main.before_request
def before_request():
    g.db = connect_db()


@main.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@main.route('/')
def homepage():
    return render_template('main/index.html')


@main.route('/entries')
def show_entries():
    print 'hello from show_entries'
    current_app.logger.info('in show_entries')
    try:
        cur = g.db.cursor()
        cur.execute('select title, text from entries order by id desc')
        entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
        return render_template('main/show_entries.html', entries=entries)
    except Exception as e:
        current_app.logger.error(e.message, exc_info=e)


@main.route('/projects')
def show_projects():
    try:
        session = models.create_session(models.DB_URL)
        projects = session.query(models.Project).order_by(models.Project.id)
        return render_template('main/show_projects.html', projects=projects)
    except Exception as e:
        current_app.logger.error(e.message, exc_info=e)


@main.route('/projects/<project_slug>')
def show_project(project_slug):
    try:
        session = models.create_session(models.DB_URL)
        project = session.query(models.Project).filter_by(slug=project_slug).first()
        return render_template('main/show_project.html', project=project)
    except Exception as e:
        current_app.logger.error(e.message, exc_info=e)


@main.route('/regions/<region_slug>')
def show_region(region_slug):
    try:
        session = models.create_session(models.DB_URL)
        region = session.query(models.Region).filter_by(slug=region_slug).first()
        return render_template('main/show_region.html', region=region)
    except Exception as e:
        current_app.logger.error(e.message, exc_info=e)


@main.route('/regions/<region_slug>/download')
def download_region(region_slug):
    try:
        session = models.create_session(models.DB_URL)
        region = session.query(models.Region).filter_by(slug=region_slug).first()
        outfile = StringIO.StringIO()
        writer = unicodecsv.writer(outfile)
        header = ('ptolemy_id', 'ptolemy_name', 'modern_name', 'ptolemy_lat', 'ptolemy_lon', 'modern_lat', 'modern_lon', 'disposition')
        writer.writerow(header)
        for place in region.places:
            ptolemy_coords = to_shape(place.ptolemy_point)
            ptolemy_lat = ptolemy_coords.y
            ptolemy_lon = ptolemy_coords.x
            if place.modern_point is not None:
                modern_coords = to_shape(place.modern_point)
                modern_lat = modern_coords.y
                modern_lon = modern_coords.x
            else:
                modern_coords = None
                modern_lat = None
                modern_lon = None
            row = (place.ptolemy_id,
                   place.ptolemy_name,
                   place.modern_name,
                   ptolemy_lat,
                   ptolemy_lon,
                   modern_lat,
                   modern_lon,
                   place.disposition)
            writer.writerow(row)
        response = make_response(outfile.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=%s.csv' % (region.slug)
        response.headers['Content-type'] = 'text/csv'
        session.close()
        return response
    except Exception as e:
        current_app.logger.error(e.message, exc_info=e)


@main.route('/places')
def show_places():
    try:
        session = models.create_session(models.DB_URL)
        places = session.query(models.Place).order_by(models.Place.ptolemy_id)
        return render_template('main/show_entries.html', places=places)
    except Exception as e:
        current_app.logger.error(e.message, exc_info=e)


@main.route('/places/<ptolemy_id>')
def show_place(ptolemy_id):
    try:
        session = models.create_session(models.DB_URL)
        place = session.query(models.Place).get(ptolemy_id)
        place.ptolemy_coords = to_shape(place.ptolemy_point)
        if place.modern_point is not None:
            place.modern_coords = to_shape(place.modern_point)
        else:
            place.modern_coords = None
        return render_template('main/show_place.html', place=place)
    except Exception as e:
        current_app.logger.error(e.message, exc_info=e)


@main.route('/places/<ptolemy_id>/edit')
def edit_place(ptolemy_id):
    try:
        session = models.create_session(models.DB_URL)
        place = session.query(models.Place).get(ptolemy_id)
        place.ptolemy_coords = to_shape(place.ptolemy_point)
        if place.modern_point is not None:
            place.modern_coords = to_shape(place.modern_point)
        else:
            place.modern_coords = None
        form = forms.PlaceForm(obj=place)
        return render_template('main/edit_place.html', place=place, form=form)
    except Exception as e:
        current_app.logger.error(e.message, exc_info=e)


@main.route('/places/<ptolemy_id>/save', methods=['POST'])
def save_place(ptolemy_id):
    try:
        if request.form['submit'] == 'Submit':
            session = models.create_session(models.DB_URL)
            place = session.query(models.Place).get(ptolemy_id)
            place.ptolemy_name = request.form['ptolemy_name']
            place.modern_name = request.form['modern_name']
            ptolemy_lat, ptolemy_lon = [float(s) for s in request.form['ptolemy_coords'].split(' ')]
            place.ptolemy_point = from_shape(Point(ptolemy_lon, ptolemy_lat))
            if len(request.form['modern_coords'].split(' ')) > 1:
                modern_lat, modern_lon = [float(s) for s in request.form['modern_coords'].split(' ')]
                place.modern_point = from_shape(Point(modern_lon, modern_lat))
            else:
                place.modern_point = None
            place.disposition = request.form['disposition']
            session.add(place)
            session.commit()
            session.close()
        return redirect(url_for('main.show_place', ptolemy_id=ptolemy_id))
    except Exception as e:
        current_app.logger.error(e.message, exc_info=e)



@main.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.cursor()
    cur.execute('insert into entries (title, text) values (%s, %s)',
                 [request.form['title'], request.form['text']])
    cur.close()
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@main.route('/add-entry-form', methods=['GET'])
def add_entry_form():
    return render_template('main/add_entry.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != main.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != main.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('main/login.html', error=error)


@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


