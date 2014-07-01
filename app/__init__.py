from flask import Flask
import os
import config

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object('config')

app.secret_key = config.SECRET_KEY

app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE

# Flask-SQLAlchemy
db = SQLAlchemy(app)

# Flask-Login
lm = LoginManager()
lm.init_app(app)

# Flask-Markdown
md = Markdown(app)

from app import views, models

