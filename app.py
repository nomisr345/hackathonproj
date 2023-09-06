from flask import Flask, render_template,request
import requests

app = Flask(__name__)
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
        return render_template("index.html", recipes=recipes)
    else:
        # Handle API error
        return "Failed to fetch recipes from Spoonacular API."

@app.route('/display_recommendations', methods =[ 'GET'])
def display_recommendations():
    # return render_template("recommendations.html")
    response = requests.get(
        f'https://api.spoonacular.com/recipes/complexSearch',
        params={
            'apiKey': SPOONACULAR_API_KEY,
            'number': 10,  # Number of recipes to fetch
            'sort': 'popularity',  # Sort by popularity or other criteria
        }
    )
    if response.status_code == 200:
        data = response.json()
        values = data['results']
        return render_template("recommendations.html", values = values)
    else:
        # Handle API error
        return "Failed to fetch filtered results from Spoonacular API."
@app.route('/get_recommendations')
def get_recommendations():
    return render_template('preferencespage/index.html')

@app.route("/search")
def search_page():
    return render_template('search.html')

if __name__ == "__main__":
    app.run(debug=True)
