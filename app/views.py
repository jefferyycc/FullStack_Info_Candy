"""
need to update
"""
from flask import Flask, render_template, redirect, request, session, escape, url_for
from app import app, models
from .forms import UserForm
# Access the models file to use SQL functions
from .models import *

# index page
@app.route('/')
@app.route('/index')
def index():
    """
    if 'username' in session:
        username = escape(session['username'])
        return redirect('/trips')
    else:
    """
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    print('Jump to login.html!', file=sys.stderr)
    return render_template('login.html')
    """
    if request.method=='POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('index'))
    if request.method=='GET':
        return redirect(url_for('signup'))
    """

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    print('Jump to signup.html!', file=sys.stderr)
    return render_template('signup.html')
    """
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
    """

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('index'))

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    None

#@app.route('/order')
#def display_order():
#    None

@app.route('/create-order', methods=['GET', 'POST'])
def create_order():
    None

@app.route('/remove-order/<value>')
def remove_order(value):
    None

@app.route('/choose')
def choose():
    print('Jump to choose.html!', file=sys.stderr)
    return render_template('choose.html')

# 404 errohandler
@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404
