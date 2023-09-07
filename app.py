from flask import Flask, render_template, request, flash, redirect, url_for,session
import requests
import secrets
from Forms import SearchForm

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

@app.route("/search")
def search_page():
    return render_template('search.html')

@app.route("/loginpage")
def login_page():
    return render_template('login page/loginpage.html')

if __name__ == "__main__":
    app.run(debug=True)
