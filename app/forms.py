from flask_wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import DataRequired

# IMPORTS FROM TUTORIAL DON'T WORK (CUZ OF DIFFERENT VERSION?)
# from flask.ext.wtf import Form, TextField, BooleanField
# from flask.ext.wtf import Required

class LoginForm(Form):
	openid = TextField('openid', validators = [DataRequired()])
	remember_me = BooleanField('remember_me', default = False)