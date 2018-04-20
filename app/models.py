"""
need to update
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

def retrieve_user(curr_user):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Customer WHERE email=(?)", [curr_user])
    users = cur.fetchall()
    conn.close()
    return users

# def insert_order(trip_owner, dest, trip_name, friend):

# def delete_order(value):