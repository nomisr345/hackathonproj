from db import db

class Users(db.Model):
	usr_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)
	def __repr__(self):
		return '<Name %r>' % self.username