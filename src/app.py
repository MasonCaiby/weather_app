from flask import Flask, render_template, request, flash
import sqlalchemy
import re
from database import Database

app = Flask(__name__)
app.secret_key = 'super secret key'

# I stored the cities in a csv so we wouldn't have to deal with passing a database with data around.
with open('cities.csv') as cities_file:
    cities = cities_file.read().split('\n')

database = Database()
email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' # I shamelessly stole this from the internet

@app.route('/', methods=['GET', 'POST'])
def my_form_post():

    # we only want to check for data if the user is POSTing
    if request.method == 'POST':
        email = request.form.get('email')
        city = request.form.get('city')

        # make sure we have needed data, and that the email is syntatic-ally valid.
        if (re.search(email_regex, email)) and city:
            try:
                database.add_email(email, city)
                flash(f'<SCRIPT>alert("User {email} added with City {city}")</SCRIPT>')

            # I'm just letting SQL tell me if a user is in the DB already or not. No need to do a second check
            except sqlalchemy.exc.IntegrityError:
                flash(f'<SCRIPT>alert("User {email} Already Exists.")</SCRIPT>')

        # never fail silently
        else:
            flash('<SCRIPT>alert("Please enter a valid email and City.")</SCRIPT>')

    return render_template('add_user.html', cities=cities)


if __name__ == "__main__":
    app.run()
