import flask
from flask import render_template

app = flask.Flask(__name__)

@app.route('/')
def home():import flask
from flask import render_template

app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/')
def about():
    return render_template('about.html')

@app.route('/')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)