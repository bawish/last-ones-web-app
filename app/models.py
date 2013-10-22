from app import db

# "models" are where you store info about the database schema (how info is stored and retrieved)

ROLE_USER = 0
ROLE_ADMIN = 1

# this class defines the db table describing USERS
class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	# following field is added to link users to posts they write
	# this is not an actual db field
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
	
	# tells Python how to print objects of this class
	# useful for debugging
	def __repr__(self):
		return '<User %r>' % (self.nickname)

# this class defines the db table describing POSTS
class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	# the ForeignKey below links posts to users in User class
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Post %r>' % (self.body)