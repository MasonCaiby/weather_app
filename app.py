from flask import Flask, render_template, request
from database import add_email, get_session, grab_data

app = Flask(__name__)
with open('cities.csv') as cities_file:
    cities = cities_file.read().split('\n')

data, DATABASE_URI = grab_data()

engine, Session = get_session(DATABASE_URI)

@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    email = request.form.get('email')
    city = request.form.get('city')
    print(email)
    print(city)
    if email and city:
        add_email(Session, email, city)
    return render_template('add_user.html', cities=cities)


if __name__ == "__main__":
    app.run()
