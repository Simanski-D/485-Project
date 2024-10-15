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

@app.route('/', methods=['POST', 'GET'])
def login():
    return render_template('login.html')
#change
@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST' :

        email = request.form.get('email')
        password = request.form.get('pw_key')
        confirm_password = request.form.get('confirm_pw')
        
        # Add database insertion logic
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        try:
            # Check if the username already exists
            cursor.execute("SELECT * FROM user_info WHERE email = %s", (email,))
            count = cursor.fetchone()

            if count is not None:
                # Username already exists
                flash('An account with this email already exists.', 'error')
                return redirect(url_for('login'))  # Redirect back to home if the username exists
            

            if password != confirm_password:
                #passwords don't match
                flash('Your two password entries do not match!', 'error')
                return redirect(url_for('create_account'))


            # If the username is not taken, proceed with account creation
            iterations = 100000
            key_length = 32

            salt = os.urandom(32)
            password_bytes = password.encode("utf-8")
            hashed_password = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen=key_length)

            # Store user in database
            cursor.execute("INSERT INTO user_info (email, salt, pw_key) VALUES (%s, %s, %s)", (email, salt.hex(), hashed_password.hex()))
            connection.commit()
            return redirect(url_for('login'))

        finally:
            cursor.close()
            connection.close()

    return render_template('createAccount.html')

if __name__ == '__main__':
    app.run(debug=True)