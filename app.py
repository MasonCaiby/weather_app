from flask import Flask, render_template, request

app = Flask(__name__)
cities = ['abcdef', 'testingtest']


@app.route('/', methods=['GET','POST'])
def my_form_post():
    text = request.form.get('text')

    return render_template('add_user.html')

if __name__ == "__main__":
    app.run()
