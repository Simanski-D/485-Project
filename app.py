from flask import Flask, render_template, request, redirect, url_for, session, jsonify, request,flash
import sys
from werkzeug.security import check_password_hash
from datetime import datetime
from werkzeug.security import generate_password_hash
from datetime import date
import re
import os
import sqlite3
import hashlib
import mysql.connector
from mysql.connector import Error



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'your_secret_key'

#method that establishes connection to MySQL server - user=root for now...
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", #input password
            database="ec_mysql.cs485"
        )
        if connection.is_connected():
            print("Successfully connected")
            return connection
    except Error as e:
        print(f"The error '{e}' occured")
        return None

#method to be used in signup page to create account with hashed and salted password. Stores user info and salt in DB.
@app.route('/signup', methods=['GET', 'POST'])
def account_creation():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']


        connection = create_connection()
        if connection is None:
            return
        
        cursor = connection.cursor()

        #link to html boxes with button
        user = input("Create a username:\n")
        email = input("Add your email:\n")
        pword = input("Create a password:\n")

        
        #check if username and/or is taken in database
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (user,))
        if cursor.fetchone()[0] > 0:
            print("This username is already being used")
            connection.close()
            return
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
        if cursor.fetchone()[0] > 0:
            print("This email is already being used")
            connection.close()
            return


        iterations = 100000 #more is more secure
        key_length = 32 
        salt = os.urandom(32)
        pword_bytes = pword.encode("utf-8") 
        hashed_pword = hashlib.pbkdf2_hmac('sha256', pword_bytes, salt, iterations, dklen = key_length)

        cursor.execute("Insert into users (username, email, hashed_key, salt) values (%s, %s, %s, %s)", (user, email, hashed_pword.hex(), salt.hex()))
        connection.commit()
        cursor.close()
        connection.close()

    # print(f'Salt: {salt.hex()}') 
    # print(f'Hashed password: {hashed_pword.hex()}')  #prints hashed password in hex instead of bytes

        #displays success message to user
        flash('Account successfully created', 'success')
        return redirect(url_for('login')) 
    return render_template('crudeLogIn.html')


#check username, password against DB with salt and hash
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        return f"logged in as {username}"
    
    return render_template('CrudeLogIn.html')

def is_logged_in():
    return 'user_id' in session

@app.route('/')
def index():
    if not is_logged_in():
        return redirect(url_for('login'))
    #user = User.query.get(session['user_id'])


if __name__ == '__main__':    
    # APP.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
