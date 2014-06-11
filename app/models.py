from app import db
from passlib.apps import custom_app_context as pwd_context

ROLE_USER = 0
ROLE_ADMIN = 1

# A lower level helper table to help relate the users to the tags (many-to-many)
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    # Two helper classes for easier password management
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # These are required by Flask-Login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(256)) # a blog post needs to have a title
    slug = db.Column(db.String(256)) # a slug for the post url
    body = db.Column(db.String(32768))
    description = db.Column(db.String(256)) # a small description of the post
    thumbnail = db.Column(db.String(256))   # thumbnail image for the blog post
    timestamp = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))

    def get_tags_str(self):
        # gets a list of tagnames for this post
        return [tag.name for tag in self.tags]

    def set_tags_str(self, tags):
        # sets a list of tagnames for this post

        # empty the list
        while self.tags:
            del self.tags[0]

        for name in tags:
            self.tags.append(self._get_or_create(name))

    def _get_or_create(self, tagname):
        # gets a tag by name or creates one if it isn't found

        q = Tag.query.filter_by(name=tagname)
        t = q.first()
        if not(t):
            t = Tag()
            t.name = tagname
        return t

    def __repr__(self):
        return '<Post %r>' % (self.body[:64])

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    def __repr__(self):
        return '<Tag %r>' % (self.name)
