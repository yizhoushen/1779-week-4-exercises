from flask import render_template, redirect, url_for, request, g
from app import webapp

import mysql.connector

from app.config import db_config
import sys


def connect_to_database():
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@webapp.route('/',methods=['GET'])
@webapp.route('/index',methods=['GET'])
@webapp.route('/main',methods=['GET'])

# Display an HTML page with links
def main():
    cnx = get_db()

    cursor = cnx.cursor()
    query = "SELECT id, name, quantity FROM product"
    cursor.execute(query)

    products = []
    for i in cursor:
        products.append(i)

    query = "SELECT id, name FROM customer"
    cursor.execute(query)

    customers = []
    for i in cursor:
        customers.append(i)

    return render_template("main.html",products=products,customers=customers)
