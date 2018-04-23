"""
Database functions
"""
import sqlite3 as sql
from flask import session, escape
import sys

def get_connection(db_path='app.db'):
    return sql.connect(db_path)

def check_user(email):
    """
	Check whether the email is already in the database.
	input: email
	output: boolean
	"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Customer WHERE email=(?)", [email])
    users = cur.fetchall()
    conn.close()
    return True if users else False

def insert_user(email, password, first_name, last_name, street, city, state, zip_code, phone):
	"""
	Insert user's information into Customer table and Password table.
	input: user's information
	output: None
	"""
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("INSERT INTO Customer (email, first_name, last_name, street, city, state, zip, phone) VALUES (?,?,?,?,?,?,?,?)", [email, first_name, last_name, street, city, state, zip_code, phone])
	cur.execute("INSERT INTO Password (email, password) VALUES (?,?)", [email, password])
	conn.commit()
	conn.close()

def login_check(email, password):
	"""
	Ask database whether the email and password match.
	input: user's email and password
	output: boolean
	"""
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM Password WHERE email=(?) and password=(?)", [email, password])
	info = cur.fetchall()
	conn.close()
	return True if info else False

# add method  
def get_user(email):
	"""
	Get user information using email
	input: user's email
	output: user object
	"""
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM Customer WHERE email=(?)",[email])
	info = cur.fetchall()
	conn.close()
	return info

def get_single_box(box_id):
    """
    Given box_id, return a dictionary of box information.
    input: "05050500"
    output: {'C1': 5, 'C2': 5, 'C3': 5, 'C4': 0, 'price': 36.5, 'calories': 1850, 'box_id': '05050500'}
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(Box.candy_amount*Candy.price), SUM(Box.candy_amount*Candy.calories), SUM(Box.candy_amount) FROM Box, Candy WHERE Box.box_id=(?) AND Box.candy_name=Candy.candy_name", [box_id])
    price_cal = cur.fetchall()
    cur.execute("SELECT candy_name, candy_amount FROM Box WHERE box_id=(?)", [box_id])
    candy_info = cur.fetchall()
    conn.close()
    box_info = {c[0]:c[1] for c in candy_info}
    # add one more variable
    box_info['total'] = price_cal[0][2]
    # box_info['milk'] = candy_info[0][1]
    # box_info['chocolate'] = candy_info[1][1]
    # box_info['almond'] = candy_info[2][1]
    # box_info['sugar'] = candy_info[3][1]
    box_info['price'] = price_cal[0][0]
    box_info['calories'] = price_cal[0][1]
    box_info['box_id'] = box_id
    
    return box_info

def place_order(order_info):
	"""
	Given order_info, place the order. Insert into order and item tables.
	input: {'email': 'jiaxun.song@outlook.com',
			'boxes': {'05000000': 1, '10000500': 3, '00001500': 2}, 
			'create_date': '2018-04-20 15:25:46', 
			'order_id': '0956b7a9-2fd4-35e8-8005-57633da3307d', 
			'total_price': 213.5}
	output: None
	"""
	conn = get_connection()
	cur = conn.cursor()

	order_id = order_info["order_id"]
	email = order_info["email"]
	create_date = order_info["create_date"]
	total_price = order_info["total_price"]
	paid = 0 # default unpaied
	payment_id = "" # empty until user chooses the payment method.

	cur.execute("INSERT INTO `Order` (order_id, email, create_date, total_price, paid, payment_id) VALUES (?,?,?,?,?,?)", [order_id, email, create_date, total_price, paid, payment_id])

	boxes = order_info["boxes"]
	table = [list(box) for box in boxes.items()]
	for row in table:
		row.insert(1, order_id)
	table = [str(tuple(row)) for row in table]
	cur.execute("INSERT INTO Item (box_id, order_id, quantity) VALUES " + ", ".join(table))
	conn.commit()
	conn.close()

def cancel_order(order_id):
	"""
	Given order_info, delete the order from order and item tables.
	input: order_id, e.g. "0956b7a9-2fd4-35e8-8005-57633da3307d"
	output: boolean, True if the order_id is in the database.
	"""
	conn = get_connection()
	cur = conn.cursor()

	cur.execute("SELECT * FROM `Order` WHERE order_id=(?)", [order_id])
	order = cur.fetchall() # check whether the order_id exists.

	cur.execute("DELETE FROM `Order` WHERE order_id=(?)", [order_id])
	cur.execute("DELETE FROM Item WHERE order_id=(?)", [order_id])
	conn.commit()
	conn.close()
	return True if order else False

def get_order(email):
	"""
	Given email, return user's all orders.
	input: email
	output: list of tuples. e.g.
	[('cc3d82e2-215a-3803-84de-3b1b0a17a79a', 'jiaxun.song@outlook.com', '2018-04-20 15:49:07', 575.0, 0, '')]
	"""
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM `Order` WHERE email=(?)", [email])
	orders = cur.fetchall()
	conn.close()
	return orders

def get_payment():
	"""
	input: None
	output: list of tuples. e.g. [('1', 'Venmo', 'venmo.com'), ('2', 'WeChat', 'wechat.com')]
	"""
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM Payment")
	payment_methods = cur.fetchall()
	conn.close()
	return payment_methods

def select_payment(order_id, payment_id):
	"""
	Given order_id and payment_id, insert payment_id into order table.
	input: order_id, payment_id
	output: None
	"""
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("UPDATE `Order` SET payment_id=(?) WHERE order_id=(?)", [payment_id, order_id])
	conn.commit()
	conn.close()

def check_paid(order_id):
	"""
	Given order_id check whether the order is paid.
	input: order_id
	output: boolean
	"""
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT paid FROM `Order` WHERE order_id=(?)", [order_id])
	paid = cur.fetchall()[0][0]
	conn.commit()
	conn.close()
	return True if paid else False

def pay_via_email(order_id):
	"""
	Given order_id, update paid info.
	input: order_id
	output: boolean, False if the order is already paid.
	"""
	conn = get_connection()
	cur = conn.cursor()
	if not check_paid(order_id):
		cur.execute("UPDATE `Order` SET paid=(?) WHERE order_id=(?)", [1, order_id])
		conn.commit()
		conn.close()
		return True
	return False