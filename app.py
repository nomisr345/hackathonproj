from flask import Flask, render_template, request, flash, redirect, url_for,session,send_from_directory,jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from db import db, User, Recipe, SavedRecipe, add_saved_recipe, get_saved_recipes_by_user

from helpers import login_required
import requests
import secrets
from Forms import SearchForm
import logging
import shelve, User
from saved import Saved
from flask_sqlalchemy import SQLAlchemy
from models import Users, SavedRecipes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

secret_key = secrets.token_hex(32)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_USE_SIGNER"] = True
Session(app)

app.config['SECRET_KEY'] = secret_key
SPOONACULAR_API_KEY = '0c9652ce1d1147619d550d8a1dee321e'


@app.route("/")
def index():
    response = requests.get(
        f'https://api.spoonacular.com/recipes/complexSearch',
        params={
            'apiKey': SPOONACULAR_API_KEY,
            'number': 10,  # Number of recipes to fetch
            'sort': 'healthiness',  # Sort by popularity or other criteria
        }
    )
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        recipes = data['results']

        # Print and check the recipes
        for recipe in recipes:
            print(f"Recipe ID: {recipe['id']}, Title: {recipe['title']}")

        return render_template("index.html", recipes=recipes)
    else:
        # Handle API error
        return "Failed to fetch recipes from Spoonacular API."


@app.route('/get_recommendations', methods=['GET', 'POST'])
def get_recommendations():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        maxcalories = form.maxcalories.data
        minprotein = form.minprotein.data
        maxfat = form.maxfat.data
        allergies = form.allergies.data
        preferredDiet = form.preferredDiet.data
        return redirect(url_for('display_recommendations', maxcalories=maxcalories, minprotein=minprotein, maxfat=maxfat,allergies=allergies, preferredDiet=preferredDiet))
    return render_template('preferencespage/index.html', form=form)

@app.route('/display_recommendations', methods=['GET'])
def display_recommendations():
    maxcalories = request.args.get('maxcalories')
    minprotein = request.args.get('minprotein')
    maxfat = request.args.get('maxfat')
    allergies = request.args.get('allergies')
    preferredDiet = request.args.get('preferredDiet')
    response = requests.get(
        f'https://api.spoonacular.com/recipes/complexSearch',
        params={
            'apiKey': SPOONACULAR_API_KEY,
            'maxCalories': maxcalories,
            'minProtein': minprotein,
            'maxFat': maxfat,
            'excludeIngredients': allergies,
            'diet': preferredDiet,
            'number': 20,  # Number of recipes to fetch
            'sort': 'healthiness',  # Sort by popularity or other criteria
        }
    )
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        recipes = data['results']
        return render_template('recommendations.html',
                              datas= recipes)
    else:
        return "Failed to fetch recipes from Spoonacular API."

@app.route("/search")
def search_page():
    return render_template('search.html')

@app.route("/saved")
def saved_page():
    return render_template('saved.html')
@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        session.clear()
        password = request.form.get("password")
        repassword = request.form.get("repassword")
        # if (password != repassword):
        #     return render_template("error.html", message="Passwords do not match!")

        # hash password
        pw_hash = generate_password_hash(
            password, method='pbkdf2:sha256', salt_length=8)

        fullname = request.form.get("fullname")
        username = request.form.get("username")
        # store in database
        new_user = Users(username=username, password=pw_hash)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            return render_template("error.html", message="Username already exists!")
        return render_template("signin.html", msg="Account created!")
    return render_template('login page/signup.html')

# def valid_login(username, password):
#     # Replace this with your actual login validation logic
#     # For demonstration purposes, this example uses hardcoded values
#     valid_username = "example_user"
#     valid_password = "example_password"
#
#     if username == valid_username and password == valid_password:
#         return True
#     else:
#         return False


@app.route("/signin", methods=["GET","POST"])
def signin_page():
        if request.method == "POST":
            session.clear()
            username = request.form.get("username")
            password = request.form.get("password")
            result = Users.query.filter_by(username=username).first()
            print(result)
            # Ensure username exists and password is correct
            if result == None or not check_password_hash(result.password, password):
                return render_template("error.html", message="Invalid username and/or password")
            # Remember which user has logged in
            session["username"] = session["username"] = result.username
            return redirect("/")
        return render_template("login page/signin.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    username = session.get("username")
    return f"Welcome, {username}!"


# Import necessary modules and classes

# Function to fetch saved recipes (you should implement this)
# @app.route('/save_recipe/<int:recipe_id>', methods=['POST'])
# def save_recipe(recipe_id):
#     if 'username' in session:
#         # Get the current user's ID based on the session username
#         current_user = Users.query.filter_by(username=session['username']).first()
#
#         # Check if the recipe is already saved by the user
#         existing_saved_recipe = SavedRecipes.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
#         if existing_saved_recipe:
#             # Recipe is already saved, return a JSON response indicating it's saved
#             return jsonify(saved=True)
#
#         # Create a new SavedRecipes record to save the recipe
#         saved_recipe = SavedRecipes(user_id=current_user.id, recipe_id=recipe_id)
#         db.session.add(saved_recipe)
#         db.session.commit()
#
#         # Return a JSON response indicating the recipe is now saved
#         return jsonify(saved=True)
#     else:
#         # User is not logged in, return an error JSON response
#         return jsonify(error='User not logged in')
#
# # Define a route to retrieve saved recipes for the current user
# @app.route('/saved_recipes')
# def saved_recipes():
#     if 'username' in session:
#         # Get the current user's ID based on the session username
#         current_user = Users.query.filter_by(username=session['username']).first()
#
#         # Retrieve the saved recipes for the current user
#         saved_recipe_records = SavedRecipes.query.filter_by(user_id=current_user.id).all()
#
#         # Extract the recipe IDs from the saved records
#         saved_recipe_ids = [record.recipe_id for record in saved_recipe_records]
#
#         # Retrieve the actual recipe objects from the Recipe model
#         saved_recipes = Recipes.query.filter(Recipes.id.in_(saved_recipe_ids)).all()
#
#         # Render the 'saved.html' template with the saved recipes
#         return render_template('saved.html', saved_recipes=saved_recipes)
#     else:
#         # User is not logged in, handle accordingly (redirect, show an error, etc.)
#         return redirect(url_for('login'))  # Redirect to login page or handle as needed

# Other routes and functions for your application



# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # Add other user fields (e.g., username, password, etc.)
#     saved_recipes = db.relationship('Saved', backref='user', lazy=True)


if __name__ == "__main__":
    app.run(debug=True)
