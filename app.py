from flask import Flask, render_template, request, redirect, url_for, flash
import hashlib
import os
import mysql.connector


app = Flask(__name__)
app.secret_key = 'dummy_key'  


# Database connection parameters
DB_CONFIG = {
    'host': "wayne.cs.uwec.edu",
    'user': "DENNERKW5831",  
    'password': "7Q155UGZ",  
    'database': "cs485group1", 
    'port': "3306"  
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST' :
        return render_template('CreateAccount.html')

    if request.method == 'POST' :

        email = request.form['email']
        password = request.form['password']
        
        # Add database insertion logic
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        try:
            # Check if the username already exists
            cursor.execute("SELECT COUNT(*) FROM user_info WHERE email = %s", (email,))
            count = cursor.fetchone()[0]

            if count > 0:
                # Username already exists
                flash('Email already exists! Please choose a different email.', 'error')
                return redirect(url_for('/'))  # Redirect back to home if the username exists

            # If the username is not taken, proceed with account creation
            iterations = 100000
            key_length = 32

            salt = os.urandom(32)
            password_bytes = password.encode("utf-8")
            hashed_password = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen=key_length)

            # Store user in database
            cursor.execute("INSERT INTO user_info (email, hashed_key, salt) VALUES (%s, %s, %s)", (email, hashed_password.hex(), salt.hex()))
            connection.commit()
            flash('Account created successfully!', 'success')
            
            # Redirect to the homepage after account creation
            return redirect(url_for('homepage'))

        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
            return redirect(url_for('home'))  # Redirect back to home on error
        finally:
            cursor.close()
            connection.close()
    return render_template('CreateAccount.html')

@app.route('/homepage')
def homepage():
    return render_template('dashboard.html') 

if __name__ == '__main__':
    app.run(debug=True)
