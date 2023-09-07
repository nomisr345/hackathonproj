from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    saved_recipes = db.relationship('SavedRecipe', backref='user', lazy=True)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    # Add other recipe fields (e.g., ingredients, instructions, etc.)

class SavedRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    # Add other fields as needed, such as date_saved

# Define functions for database operations
def add_saved_recipe(user_id, recipe_id):
    saved_recipe = SavedRecipe(user_id=user_id, recipe_id=recipe_id)
    db.session.add(saved_recipe)
    db.session.commit()

def get_saved_recipes_by_user(user_id):
    return SavedRecipe.query.filter_by(user_id=user_id).all()

# More functions for other database operations...
