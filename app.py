from flask import Flask, render_template, request, redirect, url_for, flash
import hashlib
import os
import random
import smtplib
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

# Function to generate a random verification code
def generate_verification_code():
    return str(random.randint(100000, 999999))  # 6-digit code

# Function to send verification email
def send_verification_email(email, verification_code):
    sender_email = "kadinstars@gmail.com"  # Replace with your sender email
    sender_password = "ogdd mayq hzbq bfvd"  # Replace with your app password
    subject = "Your Verification Code"
    message = f"Subject: {subject}\n\nYour verification code is: {verification_code}"

    smtp_servers = [
        ("smtp.gmail.com", 587),  # Try TLS
        ("smtp.gmail.com", 465),  # Try SSL
    ]

    for server_address, port in smtp_servers:
        try:
            if port == 587:  # For TLS
                with smtplib.SMTP(server_address, port) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, email, message)
                    print("Verification email sent successfully using port", port)
                    return
            elif port == 465:  # For SSL
                with smtplib.SMTP_SSL(server_address, port) as server:
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, email, message)
                    print("Verification email sent successfully using port", port)
                    return
        except Exception as e:
            print(f"Failed to send email via {server_address}:{port}. Error: {e}")

    # If all ports fail
    print("Failed to send email on all available ports.")

@app.route('/', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        try:
            # Checking the user_info database!!
            #cursor.execute("SELECT email, salt, pw_key FROM user_info WHERE email = %s", (email,))
            #result = cursor.fetchone()

            #Checking the CS_admin database!!
            cursor.execute("SELECT email, salt, pw_key FROM CS_admin WHERE email = %s", (email,))
            result_cs_admin = cursor.fetchone()

            cursor.execute("SELECT email FROM email_only WHERE email = %s", (email,))
            result_email_only = cursor.fetchone()

            if result_cs_admin is None or result_email_only is None:
                flash("Invalid email or password")
                return redirect(url_for('login'))

            db_email = result_cs_admin[0]  # We can take it from either result
            db_salt = result_cs_admin[1]
            db_hashed_password = result_cs_admin[2]

            # Hash the provided password with the stored salt
            password_bytes = password.encode('utf-8')
            salt_bytes = bytes.fromhex(db_salt)
            hashed_password = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, 100000, dklen=32)

            # Compare the hashed password with the one in the database
            if hashed_password.hex() == db_hashed_password:
                # Generate a verification code and store it in the database
                verification_code = generate_verification_code()
                send_verification_email(email, verification_code)

                # Store the verification code in a new table
                cursor.execute("""INSERT INTO email_verification(email, verification_code) VALUES (%s, %s)ON DUPLICATE KEY UPDATE verification_code = %s;
                """, (email, verification_code, verification_code))

                connection.commit()
                flash("A verification code has been sent to your email.")
                return redirect(url_for('verify', email=email))


            else:
                # If the password is incorrect, flash a message
                flash("Invalid email or password")
                return redirect(url_for('login'))

        finally:
            cursor.close()
            connection.close()

    return render_template('login.html')

@app.route('/verify', methods=['POST', 'GET'])
def verify():
    if request.method == 'POST':
        email = request.form.get('email')
        entered_code = request.form.get('verification_code')

        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT verification_code FROM email_verification WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result and result[0] == entered_code:
                # Successful verification
                cursor.execute("DELETE FROM email_verification WHERE email = %s", (email,))
                connection.commit()
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid verification code.")
                return redirect(url_for('verify', email=email))

        finally:
            cursor.close()
            connection.close()

    email = request.args.get('email')  # Get email from URL
    return render_template('verify.html', email=email)

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
            # Check if the username already exists in the user_info database!!
            #cursor.execute("SELECT * FROM user_info WHERE email = %s", (email,))
            #count = cursor.fetchone()

            # Check if the username already exists in the CS_admin database!!
            cursor.execute("SELECT * FROM CS_admin WHERE email = %s", (email,))
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
            #cursor.execute("INSERT INTO user_info (email, salt, pw_key) VALUES (%s, %s, %s)", (email, salt.hex(), hashed_password.hex()))
            #connection.commit()

            #CS_admin database!!
            cursor.execute("INSERT INTO CS_admin (email, salt, pw_key) VALUES (%s, %s, %s)", (email, salt.hex(), hashed_password.hex()))
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