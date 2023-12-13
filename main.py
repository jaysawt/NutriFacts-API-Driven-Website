from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import requests
import os


app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/list_food_items', methods=['POST', 'GET'])
def list_of_food():
    query = 'apple'
    if request.method == 'POST':
        query = request.form['search_input']
    API_KEY = os.environ.get('SPOONACULAR_KEY')
    url_items = 'https://api.spoonacular.com/food/search'
    parameters = {
        'query': query,
        'number': 6,
        'apiKey': API_KEY,
    }
    response = requests.get(url=url_items, params=parameters)
    response.raise_for_status()
    data = response.json()
    recipe = data['searchResults'][0]['results']
    simple_food = data['searchResults'][5]['results']
    all_food = recipe + simple_food
    return render_template('information.html', food=all_food, method=request.method)


@app.route('/nutrients/<nutri_id>/<name>')
def nutrient_by_id(nutri_id, name):
    url_nutrients = f'https://api.spoonacular.com/recipes/{nutri_id}/nutritionWidget.json'
    para = {
        'apiKey': os.environ.get('SPOONACULAR_KEY'),
    }
    res = requests.get(url=url_nutrients, params=para)
    res.raise_for_status()
    data_nutri = res.json()
    return render_template('nutrients.html', nutrients=data_nutri['nutrients'], properties=data_nutri['properties'],
                           flavonoids=data_nutri['flavonoids'], caloric_breakdown=data_nutri['caloricBreakdown'],
                           name=name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
