
from flask_wtf import Form
from wtforms import StringField, BooleanField

from wtforms.validators import DataRequired,Length
from app import db



class LoginForm(Form):
	openid = StringField('openid', validators = [DataRequired()])
	remember_me = BooleanField('remember_me', default = False)

class UserEditForm(Form):
	nickname = StringField('nickname', validators = [DataRequired()])
	about_me = StringField('about_me', validators = [Length(min = 0, max = 140)])

class PostForm(Form):
	post = StringField('post', validators = [DataRequired()])