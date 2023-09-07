from flask import Flask, render_template, request, flash, redirect, url_for,session,send_from_directory,jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from db import db, User, Recipe, SavedRecipe, add_saved_recipe, get_saved_recipes_by_user
from Forms import SearchForm,CreateUserForm
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
SPOONACULAR_API_KEY = 'ccfe11f1538f4680838f93c6d459c86f'


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

recipes = [
    {
        'id': 1,
        'title': 'Recipe 1',
        'image': 'recipe1.jpg',
        # Add other recipe data fields as needed
    },
    {
        'id': 2,
        'title': 'Recipe 2',
        'image': 'recipe2.jpg',
        # Add other recipe data fields as needed
    },
    # Add more recipe entries as needed
]

# Define the fetch_recipes function to return the recipe data
def fetch_recipes():
    return recipes

saved_recipes = {}

@app.route('/save_recipe/<recipe_id>', methods=['POST'])
def save_recipe(recipe_id):
    if request.method == 'POST':
        user_id = session.get('username')
        if user_id:
            saved_recipes.setdefault(user_id, []).append(recipe_id)
            print(saved_recipes)  # Print saved_recipes for debugging
            return jsonify({"saved": True})
        else:
            return jsonify({"error": "User not logged in"})

@app.route('/saved')
def saved_page():
    if 'username' in session:  # Check if the user is logged in
        username = session['username']  # Get the username from the session

        # Fetch the user's saved recipes from the database
        user = Users.query.filter_by(username=username).first()
        saved_recipes = SavedRecipes.query.filter_by(user_id=user.usr_id).all()

        return render_template('saved.html', saved_recipes=saved_recipes)
    else:
        return redirect(url_for('signin_page'))  # Redirect to the login page if the user is not logged in


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
    return render_template('dashboard.html', username=username)

from flask import render_template, request, session

@app.route('/profile')
def profile():
    # Get the username from the session (assuming you store it upon login)
    username = session.get('username')

    # Fetch the user data from the database
    user = Users.query.filter_by(username=username).first()

    return render_template('profile.html', user=user)


@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = User.User(create_user_form.username.data, create_user_form.email.data, create_user_form.password.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        return redirect(url_for('retrieve_users'))
    return render_template('createUser.html', form=create_user_form)






if __name__ == "__main__":
    app.run(debug=True)