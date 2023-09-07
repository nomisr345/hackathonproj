from db import db

class Users(db.Model):
    usr_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    saved_recipes = db.relationship('SavedRecipes', backref='user', lazy=True)

    def __repr__(self):
        return '<Name %r>' % self.username

class SavedRecipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.usr_id'), nullable=False)
    recipe_id = db.Column(db.String(255), nullable=False)
    # Add other fields related to the saved recipe, if needed
