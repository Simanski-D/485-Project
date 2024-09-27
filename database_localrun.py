#from argon2 import PasswordHasher#
import hashlib
import os
import mysql.connector

#method to be triggered by html click to create account
def account_creation():

    #PARAMETERS#

    connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Your MySQL username, root is default for XAMPP
            password="",  # Your MySQL password, by default empty for XAMPP
            database="passwords"  # Replace with your actual database name
    )

    cursor = connection.cursor()

    iterations = 100000 #more is more secure
    key_length = 32 

    user = input("Create a username:\n")
    print("Username is: " + user)
    #check if username is taken in database later

    salt = os.urandom(32)
    #stores salt with username later

    pword = input("Create a password:\n")
    print("Password is: " + pword) 
    #check if pword is taken in database later

    pword_bytes = pword.encode("utf-8") 

    hashed_pword = hashlib.pbkdf2_hmac('sha256', pword_bytes, salt, iterations, dklen = key_length)

    cursor.execute("Insert into users (email, hashed_key, salt) values (%s, %s, %s)", (user, hashed_pword.hex(), salt.hex()))
    connection.commit()

    print(f'Salt: {salt.hex()}') 
    print(f'Hashed password: {hashed_pword.hex()}')  #prints hashed password in hex instead of bytes
    

account_creation()   #run function 



