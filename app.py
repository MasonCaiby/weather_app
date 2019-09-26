from flask import Flask, render_template, request, flash
import sqlalchemy
import re
from database import Database

app = Flask(__name__)
app.secret_key = 'super secret key'

with open('cities.csv') as cities_file:
    cities = cities_file.read().split('\n')

database = Database()

email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

@app.route('/', methods=['GET', 'POST'])
def my_form_post():

    if request.method == 'POST':
        email = request.form.get('email')
        city = request.form.get('city')

        if (re.search(email_regex, email)) and city:
            try:
                database.add_email(email, city)
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

    return render_template('add_user.html', cities=cities)


if __name__ == "__main__":
    app.run()
