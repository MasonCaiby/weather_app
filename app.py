from flask import Flask, render_template, request


app = Flask(__name__)
with open('cities.csv') as cities_file:
    cities = cities_file.read().split('\n')


@app.route('/', methods=['GET','POST'])
def my_form_post():
    text = request.form.get('text')
    city = request.form.get('city')
    print(text)
    print(city)

    return render_template('add_user.html', cities=cities)


if __name__ == "__main__":
    app.run()
