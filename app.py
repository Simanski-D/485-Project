from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_cors import CORS
import hashlib
import os
import random
import smtplib
import mysql.connector
import ipaddress
import sklearn
from sklearn.preprocessing import StandardScaler,MinMaxScaler
import numpy as np
import pandas as pd
import tensorflow as tf

app = Flask(__name__)
CORS(app)
app.secret_key = 'dummy_key'  

#user input setup and model loading
upload_folder = './inputfiles/'
os.makedirs(upload_folder, exist_ok=True)

OUTPUT_FOLDER = './outputfiles/'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
model_prototype = tf.keras.models.load_model('model_prototype1.h5')

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
    sender_email = "kadinstars@gmail.com"
    sender_password = "ogdd mayq hzbq bfvd"
    subject = "Your Verification Code"
    message = f"Subject: {subject}\n\nYour verification code is: {verification_code}"

    smtp_servers = [
        ("smtp.gmail.com", 587),  # TLS
        ("smtp.gmail.com", 465),  # SSL
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

#Login html page functionality
@app.route('/', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        try:
            #Checking the CS_admin database!!
            cursor.execute("SELECT email, salt, pw_key FROM CS_admin WHERE email = %s", (email,))
            result_cs_admin = cursor.fetchone()

            cursor.execute("SELECT email FROM email_only WHERE email = %s", (email,))
            result_email_only = cursor.fetchone()

            if result_cs_admin is None or result_email_only is None:
                flash("Invalid email or password")
                return redirect(url_for('login'))

            db_email = result_cs_admin[0]
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

#Verify html page functionality
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

#Verify html page for the dashboard password reset
@app.route('/verify2', methods=['POST', 'GET'])
def verify2():
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
                return redirect(url_for('passwordReset'))
            else:
                flash("Invalid verification code.")
                return redirect(url_for('verify2', email=email))

        finally:
            cursor.close()
            connection.close()

    email = request.args.get('email')  # Get email from URL
    return render_template('verify2.html', email=email)

#password reset html page functionality
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
            return redirect(url_for('login'))
        
        finally:
            cursor.close()
            connection.close()
    
    return render_template('passwordReset.html')

#password reset email page functionality
@app.route('/passwordResetemail', methods=['POST', 'GET'])
def passwordResetemail():
    
    if request.method == 'POST':
        email = request.form.get('username')

        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        try:
            cursor.execute('SELECT * FROM cs_admin WHERE email = %s', (email,))
            result = cursor.fetchone()

            if  result is None:
                flash("The email entered does not have an account.")
                return(redirect(url_for('passwordResetemail')))        

            # Generate a verification code and store it in the database
            verification_code = generate_verification_code()
            send_verification_email(email, verification_code)

            # Store the verification code in a new table
            cursor.execute("""INSERT INTO email_verification(email, verification_code) VALUES (%s, %s)ON DUPLICATE KEY UPDATE verification_code = %s;
            """, (email, verification_code, verification_code))

            connection.commit()
            flash("A verification code has been sent to your email.")
            return redirect(url_for('verify2', email=email))
        
        finally:
            cursor.close()
            connection.close()
        
    return render_template('passwordResetemail.html')

@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    if request.method == 'GET':
        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        try:
            # SQL query to get the username and the count of occurrences
            cursor.execute("""
                            SELECT email
                            FROM cs_admin
                            ORDER BY email asc;
                            LIMIT 500
                        """)
            users = cursor.fetchall()  # Get all events (list of dictionaries)

            # Extract just the emails for displaying
            emails = [user['email'] for user in users]

        finally:
            cursor.close()
            connection.close()

        return render_template('createAccount.html', emails=emails)

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

            #CS_admin database!!
            cursor.execute("INSERT INTO CS_admin (email, salt, pw_key) VALUES (%s, %s, %s)", (email, salt.hex(), hashed_password.hex()))
            connection.commit()
            return redirect(url_for('login'))

        finally:
            cursor.close()
            connection.close()

    return render_template('createAccount.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
        if request.method == 'POST' :
            print("POST request received!")
            inputfile= request.files['inputfiles']
            if inputfile:
                
                print(f"File received: {inputfile.filename}")
                input_path= os.path.join(upload_folder,inputfile.filename)
                inputfile.save(input_path)
                with open(input_path, 'r', encoding='utf-8') as file:
                    file_contents = file.read()           
                # Check if the file is empty
                if os.stat(input_path).st_size == 0:
                    print(f"The uploaded file {inputfile.filename} is empty.")
                    return "Error: The uploaded file is empty.", 400  # Return error if the file is empty

                # Process the file (clean and predict)
                try:
                    output_file = process_file(input_path)
                    print(f"Processed file saved to: {output_file}")
                    return send_file(output_file, as_attachment=True)
                except Exception as e:
                    print(f"Error during file processing: {str(e)}")
                return f"Error during file processing: {str(e)}", 500  # Handle any errors during processing
            
        else:
            print("No file uploaded")
            return render_template('predict.html')  # Return error message if no file is uploaded
    

        return render_template('predict.html')



#Datacleaning method for user input
def clean_data(userdf):
	#clean timestamp
	userdf['@timestamp'] = pd.to_datetime(userdf['@timestamp'].str.replace(" @ ", " "), format="%b %d, %Y %H:%M:%S.%f")
	userdf['Numeric_Timestamp'] = userdf['@timestamp'].apply(lambda x: x.timestamp() if pd.notna(x) else 0)
	eps = 0.001 # 0 => 0.1¢
	userdf['Log_Numeric_Timestamp'] = np.log(userdf.pop('Numeric_Timestamp')+eps)
	columns_to_keep2 =['Log_Numeric_Timestamp', 'client.geo.location.lat', 'client.geo.location.lon','client.ip_as_int', 'event.outcome']
	#Clean Event.Outcome and Class
	userdf['event.outcome'] = userdf['event.outcome'].replace('failure', 1).replace('success', 0).replace('unknown',2)
	#Clean lat and lon
	#userdf['client.geo.location.lat'] = userdf['client.geo.location.lat'].str.encode('utf-8')
	#userdf['client.geo.location.lon'] = userdf['client.geo.location.lon'].str.encode('utf-8')

	userdf['client.ip'] = userdf['client.ip'].str.encode('utf-8')
	userdf['client.geo.location.lat'] = pd.to_numeric(userdf['client.geo.location.lat'],errors='coerce')
	userdf['client.geo.location.lon'] = pd.to_numeric(userdf['client.geo.location.lon'],errors='coerce')
	userdf['client.ip_as_int'] = userdf['client.ip'].apply(ip_to_int)
	columns_to_normalize = ['Log_Numeric_Timestamp', 'client.geo.location.lat', 'client.geo.location.lon','client.ip_as_int', 'event.outcome']
	min_max_scaler = MinMaxScaler()
	userdf[columns_to_normalize] = min_max_scaler.fit_transform(userdf[columns_to_normalize])
	userdf = userdf[columns_to_keep2]
	userdf = userdf.dropna()

	return userdf

def model_predict(userdf):
    predictions = model_prototype.predict(userdf)
    userdf['prediction_labels'] = np.where(predictions > 0.8, 'Good', 'Bad')
    return userdf

def process_file(filepath):
    userdf = pd.read_csv(filepath)
    cleaned_data = clean_data(userdf)
    predicted_data = model_predict(cleaned_data)

    # Save the processed data to a new file in the output folder
    output_filepath = os.path.join(OUTPUT_FOLDER, os.path.basename(filepath).replace('.csv', '_predicted.csv'))
    predicted_data.to_csv(output_filepath, index=False)

    return output_filepath

def ip_to_int(ip):
    # Decode if it's in byte format
    if isinstance(ip, bytes):
        ip = ip.decode('utf-8')

    # Check if the IP is valid
    try:
        return int(ipaddress.ip_address(ip))
    except ValueError:
        return None

# Display logs to dashboard
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'GET':
        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        try:
            # Fetch all usernames from the event table
            cursor.execute('SELECT DISTINCT username FROM event LIMIT 500')
            usernames = cursor.fetchall()  # List of unique usernames

            # Initialize a dictionary to store logs for each user and the count for each user
            user_logs = {}
            log_counts = {}

            for user in usernames:
                username = user['username']

                # Fetch logs and count of logs for each username
                cursor.execute("""
                    SELECT COUNT(*) AS log_count, timestamp, geoLat, geoLon, clientIP, eventOutcome 
                    FROM event 
                    WHERE username = %s
                    GROUP BY username, timestamp, geoLat, geoLon, clientIP, eventOutcome
                    LIMIT 500
                """, (username,))

                logs = cursor.fetchall()  # List of logs for the current username
                user_logs[username] = logs
                log_counts[username] = logs[0]['log_count'] if logs else 0  # Get log count for each username
                
        finally:
            cursor.close()
            connection.close()

    return render_template('dashboard.html', usernames=usernames, user_logs=user_logs, log_counts=log_counts)

@app.route('/api/points')
def get_points():
    if request.method == 'GET':
        # API endpoint to return points as JSON
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute('SELECT username, timestamp, geoLat, geoLon FROM event LIMIT 500')
            points = cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

        # Convert points to a list of dictionaries
        points_list = [{"coords": [point['geoLat'], point['geoLon']], "label": point['username'], "timestamp": point['timestamp']} for point in points]
    return jsonify(points_list)

if __name__ == '__main__':
    app.run(debug=True)
