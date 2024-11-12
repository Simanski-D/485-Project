from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import hashlib
import os
import mysql.connector
import ipaddress
import sklearn
from sklearn.preprocessing import StandardScaler,MinMaxScaler
import numpy as np
import pandas as pd
import tensorflow as tf

app = Flask(__name__)
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

@app.route('/', methods=['POST', 'GET'])
def login():
    ##CHANGED FOR TESTING
    return render_template('predict.html')
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
            cursor.execute("SELECT * FROM user_info WHERE email = %s", (email,))
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
            cursor.execute("INSERT INTO user_info (email, salt, pw_key) VALUES (%s, %s, %s)", (email, salt.hex(), hashed_password.hex()))
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
                    print(f"File contents:\n{file_contents[:200]}...")  # Print the first 200 characters to debug
            
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
            return "No file uploaded", 400  # Return error message if no file is uploaded
    

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



if __name__ == '__main__':
    app.run(debug=True)