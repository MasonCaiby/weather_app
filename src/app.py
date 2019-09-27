from flask import Flask, render_template, request, flash
import sqlalchemy
import re
from database import Database

app = Flask(__name__)
app.secret_key = 'super secret key'

with open('cities.csv') as cities_file:
    cities = cities_file.read().split('\n')

database = Database()
<<<<<<< HEAD:app.py
=======

email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
>>>>>>> 49e16dcb92620898d3ce1a8a497c882385da663d:src/app.py


@app.route('/', methods=['GET', 'POST'])
def my_form_post():

    if request.method == 'POST':
        email = request.form.get('email')
        city = request.form.get('city')

        if (re.search(email_regex, email)) and city:
            try:
                database.add_email(email, city)
<<<<<<< HEAD:app.py
                flash(f'<SCRIPT>alert("User Added With Email: {email} City: {city}")</SCRIPT>')
                return render_template('add_user.html', cities=cities)

            except sqlalchemy.exc.IntegrityError:
                print('duplicate')
                flash(f'<SCRIPT>alert("User: {email} Already Exists.")</SCRIPT>')
                return render_template('add_user.html', cities=cities)

        else:
            print('not enough info')
            flash('<SCRIPT>alert("Please enter a valid Email and City.")</SCRIPT>')
            return render_template('add_user.html', cities=cities)
=======
                flash(f'<SCRIPT>alert("User {email} added with City {city}")</SCRIPT>')

            except sqlalchemy.exc.IntegrityError:
                flash(f'<SCRIPT>alert("User {email} Already Exists.")</SCRIPT>')

        else:
            flash('<SCRIPT>alert("Please enter a valid email and City.")</SCRIPT>')
>>>>>>> 49e16dcb92620898d3ce1a8a497c882385da663d:src/app.py

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
