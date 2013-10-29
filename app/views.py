from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN

# "views" are functions that define how to create dynamic pages

@app.before_request
def before_request():
	g.user = current_user

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

# this is the method for rendering the index page
@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	posts = [
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
@oid.loginhandler # tells Flask-OpenID this is our login view function
def login():
	
	# checks to see if g.user is already logged in, redirects to index if so
	# the "g" global is set up by Flask as a place to store and share data during the life of a request
	# we will store the logged-in user here (in "g")
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index')) # "url_for" is a clean way to redirect to the index page
	
	# initiate the form object
	form = LoginForm()
	
	# here is where we validate and act on entered form data
	if form.validate_on_submit():
		
		# store the value of the "remember_me" boolean in the flask session
		# sessions are powerful -- stores data during request and any future requests made by same client (e.g. cookies)
		session['remember_me'] = form.remember_me.data
		
		# the "try_login" function initiates the openid login process
		return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
	return render_template('login.html',
		title = 'Sign In',
		form = form,
		providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
# the "resp" argument contains information from OpenID response
def after_login(resp):
	
	# just for validation; we require a valid email, obv
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))
	
	# this searches database for provided email
	user = User.query.filter_by(email = resp.email).first()
	
	# if "user" not found, we add him/her to db
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "": #some OpenID providers may not provide nickname so we create one
			nickname = resp.email.split('@')[0]
		user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
		db.session.add(user)
		db.session.commit()
	
	remember_me = False
	
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	
	# call Flask-Login's login_user function to register this as a valid login
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))

# logout function is pretty simple
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
	
# the carats indicate a variable which is fed to the user function
# eg /user/barrett will call user(barrett)
@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname = nickname).first() # search database for user
	if user == None:
		flash('User ' + nickname + ' not found.')
		return redirect(url_for('index'))
	posts = [
		{ 'author': user, 'body': 'Test post #1' },
		{ 'author': user, 'body': 'Test post #2' }
	]
	return render_template('user.html',
		user = user,
		posts = posts)