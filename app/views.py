"""
need to update
"""
from flask import Flask, render_template, redirect, request, session, escape, url_for
from app import app, models
# from .forms import UserForm, TripForm
# Access the models file to use SQL functions
from .models import *

# test
@app.route('/test/check_user')
def test_check_user():
    """
    Check whether the email is already in the database.
    """
    email = 'jiaxun.song@outlook.com'
    check = check_user(email)
    if check:
        return "<div>The email already existed in the database!<div/>"
    else:
        return "<div>You can use this email to register!<div/>"

@app.route('/test/register')
def test_register():
    """
    Insert user into database.
    """
    email = "jiaxun.song@berkeley.edu"
    password = "88888888"
    first_name = "Mike"
    last_name = "Song"
    street = "California Street 1234"
    city = "Berkeley"
    state = "CA"
    zip_code = "12345"
    phone = "5101234567"
    insert_user(email, password, first_name, last_name, street, city, state, zip_code, phone)
    return "<div>Registered successfully!<div/>"

@app.route('/test/login_check')
def test_login_check():
    """
    Ask database whether the email and password match.
    """
    email = "jiaxun.song@berkeley.edu"
    password = "88888888"
    if login_check(email, password):
        return "<div>Login successfully!<div/>"
    else:
        return "<div>Wrong email and password pair!<div/>"

# index page
@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        username = escape(session['username'])
        return redirect('/trips')
    else:
        return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method=='POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('index'))
    if request.method=='GET':
        return redirect(url_for('signup'))

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        insert_user(username, password, first_name, last_name)
        session['username'] = username
        session['first_name'] = first_name
        session['last_name'] = last_name
        session['password'] = password
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('index'))

@app.route('/choose')
def choose():
    return render_template('choose.html',user="test", cart="cart")

# @app.route('/create_user', methods=['GET', 'POST'])
# def create_user():

# @app.route('/order')
# def display_order():

# @app.route('/create-order', methods=['GET', 'POST'])
# def create_order():

# @app.route('/remove-order/<value>')
# def remove_order(value):

# # 404 errohandler
# @app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404
