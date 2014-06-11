import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'asdapw93 nq3ogfihds ofuf9q oc3wumvsid gh'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

POSTS_PER_PAGE = 5

UPLOAD_FOLDER = os.path.join(basedir, 'app', 'uploads')
THUMB_FOLDER = os.path.join(basedir, 'app', 'uploads', 'thumbs')
DEFAULT_THUMB = "/static/img/default_thumb.png"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

MAX_FILE_SIZE = 2 * 1024 * 1024 # 2 MB

TAG_DELIM = " "
