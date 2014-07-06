from app import app, db, models, lm

from flask import render_template, flash, redirect, session, url_for, request, g, url_for, send_from_directory, jsonify, make_response
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from forms import LoginForm, NewUserForm, NewPostForm
from models import User, ROLE_USER, ROLE_ADMIN
from sqlalchemy import desc
import datetime
import re
import os
from config import POSTS_PER_PAGE, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, THUMB_FOLDER, TAG_DELIM, DEFAULT_THUMB
from unicodedata import normalize
from PIL import Image
from functools import wraps

import helper

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

# WRAPPERS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.role != 1:
            flash(u'Admin role required.', 'alert-warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# VIEWS

@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    # note: currently we just filter the 'about' page out
    posts = models.Post.query.order_by(desc(models.Post.timestamp))\
    .filter(models.Post.slug != "about")\
    .paginate(page, POSTS_PER_PAGE, False)

    return render_template("index.html", posts=posts, \
                           get_username=get_username)

@app.route('/tag/<tagname>')
@app.route('/tag/<tagname>/<int:page>')
def tagged_posts(tagname, page=1):

    posts = models.Post.query.join(models.Post.tags)\
    .filter(models.Tag.name == tagname)\
    .order_by(desc(models.Post.timestamp))\
    .paginate(page, POSTS_PER_PAGE, False)

    return render_template("index.html", posts=posts, \
                           get_username=get_username, query_tag=tagname)

@app.route('/posts/<slug>')
def posts(slug):
    post = models.Post.query.filter_by(slug=slug).first()
    return render_template("post.html", post=post, get_username=get_username)

# A special 'About' page
@app.route('/about')
def about():
    post = models.Post.query.filter_by(slug='about').first()
    if not post:
        return redirect(url_for("index"))
    return render_template("post.html", post=post, get_username=get_username)

@app.route('/posts/<slug>/edit', methods=["GET", "POST"])
@login_required
def edit_post(slug):

    post = models.Post.query.filter_by(slug=slug).first()

    if g.user.id != post.user_id and g.user.role != 1:
        # post is editable, only if owner of the post or admin
        flash(u'You have no access to edit this post.', 'alert-warning')
        return redirect(url_for("posts", slug=slug))

    p = models.Post.query.filter_by(slug=slug).first()

    tags = TAG_DELIM.join(p.get_tags_str())

    form = NewPostForm(title=p.title, body=p.body, slug=p.slug, \
                       description=p.description, tags=tags)

    if form.validate_on_submit():
        p.title = form.title.data
        p.body = form.body.data
        p.slug = form.slug.data
        p.description = form.description.data
        p.edited = datetime.datetime.utcnow()

        tagnames = form.tags.data.split(TAG_DELIM)
        p.set_tags_str(tagnames)

        filename = upload_file(request)
        if filename:
            p.thumbnail = "/uploads/thumbs/" + filename

        db.session.commit()

        flash(u'Post edited succesfully', 'alert-success')

        return redirect(url_for("posts", slug=p.slug))

    return render_template("edit_post.html", form=form)

@app.route('/newpost', methods=["GET", "POST"])
@login_required
def new_post():
    form = NewPostForm()

    if form.validate_on_submit():

        p = models.Post(title=form.title.data, \
                        body=form.body.data, \
                        slug=slugify(form.title.data), \
                        description=form.description.data, \
                        timestamp=datetime.datetime.utcnow(), \
                        author=g.user)

        tagnames = form.tags.data.split(TAG_DELIM)
        p.set_tags_str(tagnames)

        filename = upload_file(request)
        if filename:
            p.thumbnail = "/uploads/thumbs/" + filename
        else:
            p.thumbnail = DEFAULT_THUMB

        db.session.add(p)
        db.session.commit()

        flash(u'New post created successfully.', 'alert-success')
        return redirect(url_for("index"))

    return render_template("new_post.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    user = models.User.query.filter_by(username=form.username.data).first()
    if form.validate_on_submit():
        rv = login_user(user)
        flash(u'Logged in as ' + user.username + '.', 'alert-success')
        return redirect(url_for("index"))

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/new", methods=["GET", "POST"])
@admin_required
def new_user():
    form = NewUserForm()

    if form.validate_on_submit():

        if not user_exists(form.username.data):
            role = models.ROLE_USER
            if form.admin.data == True:
                role = models.ROLE_ADMIN
            u = models.User(username=form.username.data, role=role)
            u.hash_password(form.password.data)

            db.session.add(u)
            db.session.commit()

            flash(u'New user created successfully.', 'alert-success')
            return redirect(url_for("index"))

        else:
            flash(u'Username is taken.', 'alert-danger')

    return render_template("new_user.html", form=form)

@app.route("/admin", methods=["GET", "POST"])
@login_required
@admin_required
def admin():
    """ A simple implementation of an admin panel """
    posts = models.Post.query.order_by(desc(models.Post.timestamp)).all()
    users = models.User.query.all()

    if request.method == "POST":    # get the AJAX

        # delete posts
        if request.form.get('type') == "DELETE_POST":
            slug = request.form.get('slug')
            p = models.Post.query.filter_by(slug=slug).first()
            db.session.delete(p)
            db.session.commit()

        # delete users
        if request.form.get('type') == "DELETE_USER":
            id = request.form.get('id')
            u = models.User.query.filter_by(id=id).first()

            if u.role != ROLE_ADMIN:
                db.session.delete(u)
                db.session.commit()
            else:
                return "error"

        # toggle admin status
        if request.form.get('type') == "TOGGLE_ADMIN":
            id = request.form.get('id')
            u = models.User.query.filter_by(id=id).first()
            role = u.role

            # toggle the user role
            if role == ROLE_ADMIN and current_user != u:
                u.role = ROLE_USER
            elif role == ROLE_USER:
                u.role = ROLE_ADMIN
            else:
                return "delete_self_error"

            db.session.commit()

            return str(u.role)

        # delete users
        if request.form.get('type') == "GET_USER_DATA":
            id = request.form.get('id')
            u = models.User.query.filter_by(id=id).first()

            d = {}

            d["name"] = u.username
            if u.role == ROLE_ADMIN:
                d["role"] = "admin"
            else:
                d["role"] = "user"
            d["posts"] = u.posts.count()

            return jsonify(d)



    return render_template("admin.html", posts=posts, users=users, \
                           get_username=get_username)

@app.route('/export/<slug>')
def export_post(slug):
    post = models.Post.query.filter_by(slug=slug).first()
    md = post.body
    response = make_response(md)
    response.headers["Content-Disposition"] = "attachment; filename=" + slug + ".md"
    return response

@app.route('/uploads/<path:filename>')
def host_img(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# HELPER FUNCITIONS HERE
# TODO: move these to helper.py

def upload_file(request):
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            crop_and_save(filename)

            flash(u'File uploaded successfully.', 'alert-success')

            return filename

def crop_and_save(filename):
    """ crops the image better suited for thumbnail and saves it """
    img = Image.open(os.path.join(UPLOAD_FOLDER, filename))
    img = helper.cropped_thumbnail(img, 100, 100)
    img.save(os.path.join(THUMB_FOLDER, filename))

@lm.user_loader
def load_user(id):
    ''' Loads the user from the database for the login manager'''
    return models.User.query.get(int(id))

def user_exists(username):
    return (models.User.query.filter_by(username=username).first() != None)

def get_username(id):
    # edit this to use the saved username
    if not id:
        return "deleted"
    user = models.User.query.get(int(id))
    return user.username

@app.before_request
def before_request():
    g.user = current_user

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)

    return unicode(delim.join(result))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

