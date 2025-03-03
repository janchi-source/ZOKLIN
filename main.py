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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/houses')
def houses():
    return render_template('houses.html')

@app.route('/garden')
def garden():
    return render_template('garden.html')

@app.route('/offices')
def offices():
    return render_template('offices.html')

@app.route('/cars')
def cars():
    return render_template('cars.html')

@app.route('/mental')
def mental():
    return render_template('mental.html')

if __name__ == '__main__':
    app.run(debug=True)