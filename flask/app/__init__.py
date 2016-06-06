

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

from flask_login import LoginManager
from flask_openid import OpenID
import os.path


app = Flask(__name__)

app.config.from_object('config') 
db = SQLAlchemy(app)

lm = LoginManager()
oid = OpenID(app, os.path.join(config.basedir, 'tmp'))

from app import views, models

lm.setup_app(app)

lm.login_view = 'login'
