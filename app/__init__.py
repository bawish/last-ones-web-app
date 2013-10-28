from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# following are for login
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

# variable for database
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# variables for login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models