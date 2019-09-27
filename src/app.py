from flask import Flask, render_template, request, flash
import sqlalchemy
import re
from database import Database

app = Flask(__name__)
app.secret_key = 'super secret key'

with open('cities.csv') as cities_file:
    cities = cities_file.read().split('\n')

database = Database()

email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


@app.route('/', methods=['GET', 'POST'])
def my_form_post():

    if request.method == 'POST':
        email = request.form.get('email')
        city = request.form.get('city')

        if (re.search(email_regex, email)) and city:
            try:
                database.add_email(email, city)
                flash(f'<SCRIPT>alert("User {email} added with City {city}")</SCRIPT>')

            except sqlalchemy.exc.IntegrityError:
                flash(f'<SCRIPT>alert("User {email} Already Exists.")</SCRIPT>')

        else:
            flash('<SCRIPT>alert("Please enter a valid email and City.")</SCRIPT>')

    return render_template('add_user.html', cities=cities)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run()
