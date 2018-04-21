"""
Web Server
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
    if check_user(email):
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
    if check_user(email):
        return "<div>The email already existed in the database!<div/>"
    else:
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

@app.route('/test/get_box')
def test_get_box():
    """
    Given box_id, return a dictionary of box information.
    The list is six default boxes.
    """
    box_id_list = ["10000000", "00100000", "00001000", "00000010", "05050500", "05000505"]
    box_info = {box_id:get_single_box(box_id) for box_id in box_id_list}
    return "<div>Boxes: {}<div/>".format(box_info)

@app.route('/test/place_order')
def test_place_order():
    """
    Given order_info, place the order.
    """
    from datetime import datetime
    import uuid
    # this dictionary comes from front-end.
    order_info = {"email" : "jiaxun.song@outlook.com", 
                  "boxes" : {"05050005" : 4, "15000000" : 2, "05001000" : 6}
                  }
    order_info["create_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order_info["order_id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, order_info["email"] + order_info["create_date"]))
    # this total_price calculating method can be used for front-end.
    order_info["total_price"] = sum([get_single_box(box[0])["price"] * box[1] for box in order_info["boxes"].items()])
    place_order(order_info)
    return "<div>Order placed! {}<div/>".format(order_info)

@app.route('/test/cancel_order')
def test_cancel_order():
    """
    Given order_id, cancel the order.
    """
    email = "jiaxun.song@outlook.com"
    orders = get_order(email)
    order_id = orders[0][0] # this is just for test. the order_id should be from front-end.
    if cancel_order(order_id):
        return "<div>Order cancelled! {}<div/>".format(order_id)
    else:
        return "<div>Order does not exist! {}<div/>".format(order_id)

@app.route('/test/get_order')
def test_get_order():
    """
    Given order_id, cancel the order.
    """
    email = "jiaxun.song@outlook.com"
    orders = get_order(email)
    return "<div>Orders of {}: {}<div/>".format(email, orders)

@app.route('/test/get_payment')
def test_get_payment():
    """
    Return all payment methods.
    """
    payment_methods = get_payment()
    return "<div>Payment methods: {}<div/>".format(payment_methods)

@app.route('/test/select_payment')
def test_select_payment():
    """
    When a user clicks the payment option, update payment information in the database.
    """
    email = "jiaxun.song@outlook.com"
    orders = get_order(email)
    order_id = orders[0][0] # this is just for test. the order_id should be from front-end.
    payment_id = "1"
    select_payment(order_id, payment_id)
    return "<div>Payment selected! {} {}<div/>".format(order_id, payment_id)

@app.route('/test/check_paid')
def test_check_paid():
    """
    Given order_id check whether the order is paied.
    """
    email = "jiaxun.song@outlook.com"
    orders = get_order(email)
    order_id = orders[0][0] # this is just for test. the order_id should be from front-end.
    if check_paid(order_id):
        return "<div>Paid! {}<div/>".format(order_id)
    else:
        return "<div>Unpaid! {}<div/>".format(order_id)

@app.route('/test/pay_via_email')
def test_pay_via_emaild():
    """
    Given order_id, update paid info.
    """
    email = "jiaxun.song@outlook.com"
    orders = get_order(email)
    order_id = orders[0][0] # this is just for test. the order_id should be from front-end.
    if pay_via_email(order_id):
        return "<div>Paid Successfully! {}<div/>".format(order_id)
    else:
        return "<div>This order is already paid! {}<div/>".format(order_id)
###################################################################

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
