from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
import hashlib
import os
import mysql.connector


app = Flask(__name__)
CORS(app) #allows cross origin for map -- javascript -- can eventually have specific domains allowed
app.secret_key = 'dummy_key'  


# Database connection parameters
DB_CONFIG = {
    'host': "wayne.cs.uwec.edu",
    'user': "DENNERKW5831",  
    'password': "7Q155UGZ",  
    'database': "cs485group1", 
    'port': "3306"  
}

#password reset
@app.route('/passwordReset', methods=['POST', 'GET'])
def passwordReset():
    
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_pw')

        if password != confirm_password:
            flash("Passwords do not match")  # Flash the message
            return redirect(url_for('passwordReset'))

        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        try:
            cursor.execute('SELECT * FROM cs_admin WHERE email = %s', (email,))
            result = cursor.fetchone()

            if  result is None:
                flash("The email entered does not have an account.")
                return(redirect(url_for('passwordReset')))
            
            db_email, db_salt, db_hashed_password = result
            password_bytes = password.encode('utf-8')
            salt_bytes = bytes.fromhex(db_salt)
            hashed_password = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, 100000, dklen=32)

            #changes password for email fetched
            cursor.execute('UPDATE cs_admin SET pw_key = %s WHERE email = %s', (hashed_password.hex(), email))
            connection.commit()
            print("", email)
            print("", password)
            if cursor.rowcount == 0:
                print("It didn't work")
            else:
                print("it did work", cursor.rowcount)
            return redirect(url_for('login'))
        
        finally:
            cursor.close()
            connection.close()
    
    return render_template('passwordReset.html')

@app.route('/', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        try:
            # Query the database to check if the user exists
            cursor.execute("SELECT email, salt, pw_key FROM cs_admin WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result is None:
                # If no user is found, flash a message
                flash("Invalid email or password")
                return redirect(url_for('login'))

            db_email, db_salt, db_hashed_password = result

            # Hash the provided password with the stored salt
            password_bytes = password.encode('utf-8')
            salt_bytes = bytes.fromhex(db_salt)
            hashed_password = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, 100000, dklen=32)

            # Compare the hashed password with the one in the database
            if hashed_password.hex() == db_hashed_password:
                # Redirect to the dashboard upon successful login
                return redirect(url_for('dashboard'))
            else:
                # If the password is incorrect, flash a message
                flash("Invalid email or password")
                return redirect(url_for('login'))

        finally:
            cursor.close()
            connection.close()

    return render_template('login.html')

#change
@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST' :

        email = request.form.get('email')
        password = request.form.get('pw_key')
        confirm_password = request.form.get('confirm_pw')
        

        if not email.endswith("@uwec.edu"):
            flash("Email must end with @uwec.edu")
            return redirect(url_for('create_account'))
        
        if password != confirm_password:
            flash("Passwords do not match")  # Flash the message
            return redirect(url_for('create_account'))
        

        # Add database insertion logic
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        try:
            # Check if the username already exists
            cursor.execute("SELECT * FROM cs_admin WHERE email = %s", (email,))
            count = cursor.fetchone()

            if count is not None:
                # Username already exists
                flash("An account with this email already exists.")
                return redirect(url_for('login'))  # Redirect back to home if the username exists
            
        
            # If the username is not taken, proceed with account creation
            iterations = 100000
            key_length = 32

            salt = os.urandom(32)
            password_bytes = password.encode("utf-8")
            hashed_password = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen=key_length)

            # Store user in database
            cursor.execute("INSERT INTO cs_admin (email, salt, pw_key) VALUES (%s, %s, %s)", (email, salt.hex(), hashed_password.hex()))
            connection.commit()
            return redirect(url_for('login'))

        finally:
            cursor.close()
            connection.close()

    return render_template('createAccount.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)