#from argon2 import PasswordHasher#
import hashlib
import os

#method to be triggered by html click to create account
def account_creation():

    #PARAMETERS#

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


    print(f'Salt: {salt.hex()}') 
    print(f'Hashed password: {hashed_pword.hex()}')  #prints hashed password in hex instead of bytes
    

account_creation()   #run function 




