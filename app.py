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
app.secret_key = 'dummy_key'  


# Database connection parameters + method
def create_connection():
        connection = None

        try:
            connection = mysql.connector.connect(
    
            host = "wayne.cs.uwec.edu",
            user = "DENNERKW5831",
            password = "7Q155UGZ",  
            database = "cs485group1",
            port = "3306"  
            )
            if connection.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

@app.route('/')
def index():
    if not is_logged_in():
        return redirect(url_for('login'))
    #user = User.query.get(session['user_id'])

def is_logged_in() :
    return 'user_id' in session

@app.route('/create_account', methods=['POST','GET'])
def create_account():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        connection = connection.cursor()
        if connection is None:
            flash('Database connection failed', 'error')
            return redirect(url_for('login'))
        #cursor = None
    try:
            
        cursor = connection.cursor()
    
        # Add database insertion logic
        #connection = mysql.connector.connect(**DB_CONFIG)

          #check if username and/or is taken in database
        cursor.execute("SELECT COUNT(*) FROM user_info WHERE username = %s", (user,))
        if cursor.fetchone()[0] > 0:
            flash('Username already exists! Please choose a different username.', 'error')
            connection.close()
            return redirect(url_for('login'))
        
        cursor.execute("SELECT COUNT(*) FROM user_info WHERE email = %s", (email,))
        if cursor.fetchone()[0] > 0:
            flash('Username already exists! Please choose a different username.', 'error')
            connection.close()
            return redirect(url_for('login'))

        # If the username is not taken, proceed with account creation
        iterations = 100000
        key_length = 32
    
        salt = os.urandom(32)
        password_bytes = password.encode("utf-8")
        hashed_password = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen=key_length)
    
        # Store user in database
        cursor.execute("INSERT INTO user_info (username, email, hashed_key, salt) VALUES (%s, %s, %s)", (username, email, hashed_password.hex(), salt.hex()))
        connection.commit()
        flash('Account created successfully!', 'success')

    except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
            return redirect(url_for('login'))  # Redirect back to home on error
    finally:
            cursor.close()
            connection.close()
        
        # Redirect to the homepage after account creation
    return render_template(url_for('CreateAccount.html'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        return f"logged in as {username}"
    
    return render_template('CrudeLogIn.html')

if __name__ == '__main__':
    app.run(debug=True)
