from flask import Flask, escape, render_template, request, jsonify,url_for,session,redirect

from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

import pickle

import pandas as pd

import csv

import random



import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')


vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# from log import LogisticRegression

model = pickle.load(open("finalized_model.pkl", "rb"))

data = pd.read_csv("news.csv")

with open('enews.csv', encoding="UTF-8") as file:
    reader = csv.reader(file)

    next(reader)

    readers = list(reader)
    print(random.choice(readers))
    # print(readers[1])

    # count = 0
    mylist = []
    for row in readers:
        title = (row[2] + "" + row[1])
        # print(title)
        mylist.append(title)
    print(mylist)
    filtered_text_list = []
    for text in mylist:
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(' +', ' ', text)
        words = nltk.word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word not in stop_words]
        filtered_text = " ".join(filtered_words)
        filtered_text_list.append(filtered_text)

    print(filtered_text_list)

app = Flask(__name__)

app.secret_key = 'xyzsdfg'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('index.html', mesage=mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage=mesage)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password,))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage=mesage)


@app.route("/get_random_number")
def get_random_number():
    return jsonify(random_text=random.choice(filtered_text_list))

@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/prediction', methods=["GET", "POST"])
def prediction():


    if request.method == "POST":
        news = request.form['news']
        print(news)
        predict = model.predict(vectorizer.transform([news]))[0]
        print(predict)
        if predict == 0:
            return render_template("prediction.html", prediction_text="The News is Real News📰")
        else :
            return render_template("prediction.html", prediction_text="The News is Fake News📰")
    else:
        return render_template("prediction.html")



if __name__ == '__main__':
    app.run(debug=True)
