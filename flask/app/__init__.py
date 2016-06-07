

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
import config

from flask_login import LoginManager
from flask_openid import OpenID
import os.path

from sqlalchemy import event
from sqlalchemy.engine import Engine

app = Flask(__name__)

app.config.from_object('config') 
db = SQLAlchemy(app)

lm = LoginManager()
oid = OpenID(app, os.path.join(config.basedir, 'tmp'))

from app import views, models

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
	context._query_start_time = time.time()
	app.logger.debug("Start Query:\n%s" % statement)
	# Modification for StackOverflow answer:
	# Show parameters, which might be too verbose, depending on usage..
	app.logger.debug("Parameters:\n%r" % (parameters,))


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
	total = time.time() - context._query_start_time
	app.logger.debug("Query Complete!")

	# Modification for StackOverflow: times in milliseconds
	app.logger.debug("Total Time: %.02fms" % (total*1000))

lm.setup_app(app)

lm.login_view = 'login'


if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('tmp/info.log', 'a', 1*1024*1024, 10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('....system startup.....')