from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def buttons():
    s = Session()
    return render_template('survey.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
