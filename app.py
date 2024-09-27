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
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Instance', 'site.db')
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        return f"logged in as {username}"
    
    return render_template('login.html')

def is_logged_in():
    return 'user_id' in session

@app.route('/')
def index():
    if not is_logged_in():
        return redirect(url_for('login'))
    #user = User.query.get(session['user_id'])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # APP.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)

