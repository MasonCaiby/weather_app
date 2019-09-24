from flask import Flask, render_template, request, jsonify
import re


app = Flask(__name__)
with open('cities.csv') as cities_file:
    cities = cities_file.read().split()
cities = ['abcdef', 'testingtest']


@app.route('/', methods=['GET','POST'])
def my_form_post():
    text = request.form.get('text')
    city = request.form.get('city')
    print(text)
    print(city)

    return render_template('add_user.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = [city for city in cities if re.search(f'^{search}.*', city)]

    print(f'search: {search}   query{query}')
    return jsonify(matching_results=query)

if __name__ == "__main__":
    app.run()
