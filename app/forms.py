from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from app import models

#from flask.ext.pagedown.fields import PageDownField

from flask import flash

class LoginForm(Form):
    username = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)

        if not rv:
            flash(u'Please fill in the both fields.', 'alert-danger')
            return False

        user = models.User.query.filter_by(
            username=self.username.data).first()

        if user is not None and user.verify_password(self.password.data):
            self.user = user
            return True

        flash(u'You failed with credentials', 'alert-danger')

        return False

class NewUserForm(Form):
    username = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    password2 = PasswordField('Password', [DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)

        if not rv:
            flash(u'Please fill in all the fields.', 'alert-danger')
            return False

        if self.password.data != self.password2.data:
            flash(u'Check the password fields', 'alert-danger')
            return False

        return True

class NewPostForm(Form):
    title = TextField('Title', [DataRequired()])
    body  = TextAreaField('Text', [DataRequired()])
    # body = PageDownField('Text', [DataRequired()])
    description = TextAreaField('Description', [DataRequired()])
    slug = TextField('URL Slug')
    tags = TextField('Tags')
    # thumbnail = TextField('Thumbnail URL')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)

        if not rv:
            flash(u'Please fill in all the fields.', 'alert-danger')
            return False

        return True
