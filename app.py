from flask import Flask, render_template, request, flash
import sqlalchemy
import re
from database import add_email, get_session, grab_data

app = Flask(__name__)
app.secret_key = 'super secret key'

with open('cities.csv') as cities_file:
    cities = cities_file.read().split('\n')

data, DATABASE_URI = grab_data()

engine, Session = get_session(DATABASE_URI)

email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

@app.route('/', methods=['GET', 'POST'])
def my_form_post():

    if request.method == 'POST':
        email = request.form.get('email')
        city = request.form.get('city')

        if (re.search(email_regex, email)) and city:
            try:
                add_email(Session, email, city)
                flash('<SCRIPT>alert("User Added")</SCRIPT>')
                return render_template('add_user.html', cities=cities)
            except sqlalchemy.exc.IntegrityError:
                flash('<SCRIPT>alert("User Already Exists.")</SCRIPT>')
                return render_template('add_user.html', cities=cities)
        else:
            flash('<SCRIPT>alert("Please enter a valid email and City.")</SCRIPT>')
            return render_template('add_user.html', cities=cities)

    return render_template('add_user.html', cities=cities)


if __name__ == "__main__":
    app.run()
