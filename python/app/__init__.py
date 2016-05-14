from flask import Flask

from main.controllers import main

# configuration
DATABASE = '/tmp/app.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)


app.register_blueprint(main)