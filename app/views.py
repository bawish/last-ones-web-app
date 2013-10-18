from flask import render_template, flash, redirect
from app import app
from forms import LoginForm

# this is the method for rendering the index page
@app.route('/')
@app.route('/index')
def index():
	user = { 'nickname': 'Barrett' } #fake user
	posts = [ # fake array of posts
		{
			'author': { 'nickname': 'John'},
			'body': 'Beautiful day in portland!'
		},
		{
			'author': { 'nickname': 'Susan'},
			'body': 'The Avengers movie sucked'
		}
	]
	return render_template("index.html",
		title = 'Home',
		user = user,
		posts = posts)

# method for rendering the log in page
@app.route('/login', methods = ['GET', 'POST'])
def login():
	
	# initiate the form object
	form = LoginForm()
	
	# here is where we validate and act on entered form data
	if form.validate_on_submit():
		flash("Login requested for OpenID='" + form.openid.data + "', \
			remember_me=" + str(form.remember_me.data))
		return redirect('/index')
	return render_template('login.html',
		title = 'Sign In',
		form = form,
		providers = app.config['OPENID_PROVIDERS'])