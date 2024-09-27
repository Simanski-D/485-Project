from flask import Flask, render_template, request, redirect, url_for, session, jsonify, request
import sys
from werkzeug.security import check_password_hash
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import re
import os
import sqlite3



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        return f"logged in as {username}"
    
    return render_template('login.html')


if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
