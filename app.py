from flask import Flask, render_template, request, flash, redirect, url_for,session,send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from db import db_init, db as db_sql
from helpers import login_required
import requests
import secrets
from Forms import SearchForm
import logging
import shelve, User
from models import Users

# Configure logging
logging.basicConfig(level=logging.DEBUG)

secret_key = secrets.token_hex(32)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

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
            'sort': 'popularity',  # Sort by popularity or other criteria
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
            'number': 10,  # Number of recipes to fetch
            'sort': 'popularity',  # Sort by popularity or other criteria
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
@app.route("/saved")
def saved_page():
    return render_template('saved.html')
@app.route("/search")
def search_page():
    return render_template('search.html')

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
            db_sql.session.add(new_user)
            db_sql.session.commit()
        except Exception as e:
            return render_template("error.html", message="Username already exists!")
        return render_template("login page/signin.html", msg="Account created!")
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
            session["username"] = result.username
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


if __name__ == "__main__":
    app.run(debug=True)
