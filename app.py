from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import secrets
from Forms import SearchForm
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

secret_key = secrets.token_hex(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
SPOONACULAR_API_KEY = '090e79deb937480d95c675344c10bf55'


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


@app.route('/display_recommendations', methods=['GET', 'POST'])
def display_recommendations():
    form = SearchForm()
    if form.validate_on_submit():
        # Retrieve input values
        maxcalories = form.maxcalories.data
        minprotein = form.minprotein.data
        maxfat = form.maxfat.data
        allergies = form.allergies.data
        preferredDiet = form.preferredDiet.data

        response = requests.get(
            f'https://api.spoonacular.com/recipes/complexSearch',
            params={
                'apiKey': SPOONACULAR_API_KEY,
                'diet':preferredDiet,
                'minProtein': minprotein,
                # 'maxFat':maxfat,
                # 'maxCalories':maxcalories,
                # 'excludeIngredients':allergies,
                'number': 10,  # Number of recipes to fetch
                'sort': 'popularity',  # Sort by popularity or other criteria
            }
        )
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            print(data)
            return render_template('recommendations.html', result=data)
        else:
            return 'oops no form'
    return render_template('recommendations.html',  form = form)


@app.route('/get_recommendations')
def get_recommendations():
    return render_template('preferencespage/index.html')


@app.route("/search")
def search_page():
    return render_template('search.html')

@app.route("/loginpage")
def login_page():
    return render_template('login page/loginpage.html')

if __name__ == "__main__":
    app.run(debug=True)
