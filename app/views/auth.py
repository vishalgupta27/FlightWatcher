import os
import re
from app import app
from flask import render_template, flash, session, redirect, request, url_for, jsonify
import json
import requests




with open('app/credentials.json') as f:
    data = json.load(f)
def is_valid_email(email):
    # Use regex to validate the email format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


@app.route('/')
def first_route():
    # Check if the user is logged in
    if session.get('logged_in'):

        return redirect('get_data_from_api')
    else:
        # User is not logged in, redirect to the login page
        return redirect('login')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password, "nn")

        if not is_valid_email(email):
            flash('Invalid email format. Please enter a valid email address.', 'error')
            return redirect('login')

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return redirect('login')

        if email == data['email'] and password == data['password']:
            # Store the user as logged in using Flask's session
            session['logged_in'] = True
            session['is_admin'] = True
            session['email'] = email
            return redirect('/flights')
        else:
            flash('Invalid Email and password', 'error')
            return render_template('auth/login.html')

    return render_template('auth/login.html')


@app.route('/update_password', methods=['GET', 'POST'])
def updatePasswordView():
    if request.method == 'POST':
        current_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['new_conf_password']

        if len(new_password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return redirect('update_password')

        if current_password != data['password']:
            flash('Invalid old password. Please try again.', 'error')
            return redirect('update_password')

        if new_password != confirm_password:
            flash('New passwords do not match. Please try again.', 'error')
            return redirect('update_password')

        # Update the user's password (replace this with your password update logic)
        data['password'] = new_password
        with open('app/credentials.json', 'w') as f:
            json.dump(data, f)

        flash('Password updated successfully!', 'success')
        return redirect('login')
    return render_template('auth/forgot-password.html')


@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session and log the user out
    session.clear()
    flash("You have successfully logged out!", "success")
    return redirect(url_for('login'))
