"""
Web Server
"""
from flask import Flask, render_template, redirect, request, session, escape, url_for
from app import app, models
import requests
import os
import json
from datetime import datetime
import uuid
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
def main():
    return render_template('welcome.html')

@app.route('/login',methods=['GET'])
def show_login():
    return render_template('login.html')

@app.route('/register',methods=['GET'])
def show_register():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    street = request.form.get("street")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip_code")
    phone = request.form.get("phone")
    if check_user(email):
        return render_template("register.html", message="The email already existed in database! Click here to ",login="Log In")
    else:
        insert_user(email, password, first_name, last_name, street, city, state, zip_code, phone)
        return redirect(url_for('show_login'))

@app.route('/login',methods=['POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    if login_check(email, password):
        session['email'] = email
        return redirect(url_for('choose'))
    else:
        return render_template("login.html", message="Your password is not correct.")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template("login.html", message="You've logged out.")

@app.route('/choose',methods=['GET'])
def choose():
    email = session['email']
    info = get_user(email)
    return render_template('choose.html',user=info[0][1])

@app.route('/default',methods=['GET'])
def show_default():
    email = session['email']
    box_id_list = ["10000000", "00100000", "00001000", "00050505", "05050500", "05000505"]
    box_info = {box_id:get_single_box(box_id) for box_id in box_id_list}
    info = get_user(email)
    return render_template('defaultbox.html',box1=box_info["10000000"],box2=box_info["00100000"],box3=box_info["00001000"],
        box4=box_info["00050505"],box5=box_info["05050500"],box6=box_info["05000505"],user=info[0][1])

@app.route('/diy',methods=['GET'])
def show_diy():
    email = session['email']
    info = get_user(email)
    return render_template('diy.html', user=info[0][1])

@app.route('/order',methods=["POST", "GET"])
def order():
    email = session['email']
    info = get_user(email)
    orders = get_order(email)
    return render_template('order.html', orders=orders,user=info[0][1])

@app.route('/shoppingcart', methods=['POST', 'GET'])
def shoppingcart():
    email = session['email']
    info = get_user(email)
    return render_template('shoppingcart.html', user=info[0][1])

@app.route('/thank_you/<payment_id>', methods=['GET'])
def thank_you(payment_id):
    email = session['email']
    info = get_user(email)
    first_name = info[0][1]
    orders = get_order(email)
    unpaid_orders = []
    for order in orders:
        if order[4] == 0:
            unpaid_orders.append(order)
    total_price = sum([order[3] for order in unpaid_orders])

    payment_methods = get_payment()
    for p in payment_methods:
        if p[0] == payment_id:
            payment = p[1]

    # send email
    with open(os.getcwd() + "/app/static/email.html", "r") as f:
        email_html = f.read()
    content = email_html.format(first_name, total_price, payment)

    from_email = "postmaster@sandbox37bfe0bbc27143a28e15b714ac3bc553.mailgun.org"
    data = {
        'from': from_email,
        'to': email,
        'subject': 'Your order is on the way!',
        'html': content
        }
    auth = ("api", "key-a92702a0870a9860418201112a5956c4")
    domain = "sandbox37bfe0bbc27143a28e15b714ac3bc553.mailgun.org"
    r = requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(domain),
        auth=auth,
        data=data)

    # update database
    for o in unpaid_orders:
        order_id = o[0]
        pay_via_email(order_id)
        select_payment(order_id, payment_id)
    return render_template('thankyou.html')

@app.route('/thankyou',methods=['POST'])
def thankyou():
    return render_template('thankyou2.html')

@app.route('/price_calculate', methods=['POST'])
def price_calculate():
    """
    Given dictionary of box information
    Return total price.
    """
    box_info = request.get_json()
    box_id_list = [box_id for box_id in box_info]
    price_full = [get_single_box(box_id)["price"] * box_info[box_id] for box_id in box_id_list]
    price = sum(price_full)
    return json.dumps({"price":price, "itemprice":price_full})

@app.route('/place_order', methods=['POST'])
def place_orders():
    """
    Given order_info, place the order.
    """
    # this dictionary comes from front-end.
    email = session['email']
    order_info = request.get_json()
    order_info["email"] = email
    order_info["create_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order_info["order_id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, order_info["email"] + order_info["create_date"]))
    # this total_price calculating method can be used for front-end.
    order_info["total_price"] = sum([get_single_box(box[0])["price"] * box[1] for box in order_info["boxes"].items()])
    place_order(order_info)
    return "True"

@app.route('/get_email', methods=['POST'])
def get_email():
    """
    Give js the email in flask session.
    """
    email = session['email']
    return json.dumps({"email" : email})

@app.route('/cancelorder', methods=['POST'])
def cancelorder():
    """
    Given order_id, cancel the order.
    """
    email = session['email']
    orders = get_order(email)
    order_id = request.get_json()
    cancel_order(order_id)
    return "True"
    # if cancel_order(order_id):
    #     return "<div>Order cancelled! {}<div/>".format(order_id)
    # else:
    #     return "<div>Order does not exist! {}<div/>".format(order_id)