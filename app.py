from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def my_form_post():
    try:
        text = request.form['text']
        processed_text = text.upper()
        print(processed_text)
    except Exception as e:
        print(e)
    return render_template('add_user.html')

if __name__ == "__main__":
    app.run()
