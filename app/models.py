"""
need to update
"""
import sqlite3 as sql
from flask import session, escape
import sys

"""
def insert_order(trip_owner, dest, trip_name, friend):

def delete_order(value):

def retrieve_user(curr_user):
"""

def insert_user(username, password, first_name, last_name):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, password, first_name, last_name) VALUES (?,?,?,?)", (username, password, first_name, last_name))
        con.commit()
