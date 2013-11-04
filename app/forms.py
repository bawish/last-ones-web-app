from flask_wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

# IMPORTS FROM TUTORIAL DON'T WORK (CUZ OF DIFFERENT VERSION)
# from flask.ext.wtf import Form, TextField, BooleanField
# from flask.ext.wtf import Required

# we import this class (and the form variables) in views.py
class LoginForm(Form):
	openid = TextField('openid', validators = [DataRequired()])
	remember_me = BooleanField('remember_me', default = False)

class EditForm(Form):
	nickname = TextField('nickname', validators = [DataRequired()])
	about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])