from flask import render_template, redirect, url_for, request, g
from app import webapp

import mysql.connector

import re

from app.config import db_config

def connect_to_database():
    return mysql.connector.connect(user=db_config['user'], 
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'],
                                   autocommit=True)

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

@webapp.route('/customer',methods=['GET'])
# Display an HTML list of all customer.
def customer_list():
    cnx = get_db()

    cursor = cnx.cursor()

    query = "SELECT * FROM customer"

    cursor.execute(query)

    return render_template("customer/list.html",title="Customer List", cursor=cursor)


@webapp.route('/customer/<int:id>',methods=['GET'])
#Display details about a specific customer.
def customer_view(id):
    cnx = get_db()

    cursor = cnx.cursor()

    query = "SELECT * FROM customer WHERE id = %s"

    cursor.execute(query,(id,))
    
    row = cursor.fetchone()
    
    id = row[0]
    name = row[1]
    email = row[2]

    query = '''SELECT p.id, p.name
               FROM product as p join customer_has_product cp
               ON p.id = cp.product_id
               WHERE cp.customer_id = %s'''

    products = []

    cursor.execute(query,(id,))
    
    for row in cursor:
        products.append(row)
        

    return render_template("customer/view.html",title="Customer Details",
                           products=products,
                           id=id,
                           name=name, email=email)
    

@webapp.route('/customer/edit/<int:id>',methods=['GET'])
# Display an editable HTML form populated with customer data. 
def customer_edit(id):
    cnx = get_db()

    cursor = cnx.cursor()

    query = "SELECT * FROM customer WHERE id = %s"

    cursor.execute(query,(id,))
    
    row = cursor.fetchone()
    
    id = row[0]
    name = row[1]
    email = row[2]

    return render_template("customer/edit.html",title="Edit Customer",id=id,name=name,
                           email=email)

@webapp.route('/customer/edit/<int:id>',methods=['POST'])
# Save the form changes for a particular customer to the database.
def customer_edit_save(id):
    name = request.form.get('name',"")
    email = request.form.get('email',"")

    error = False

    if name == "" or email== "":
        error=True
        error_msg="Error: All fields are required!"

   
    if error:
        return render_template("customer/edit.html",title="Edit Customer",error_msg=error_msg, id=id,
                               name=name, email=email)


    cnx = get_db()
    cursor = cnx.cursor()

    query = ''' UPDATE customer SET name=%s, email=%s
                WHERE id = %s '''
    
    cursor.execute(query,(name,email,id))
    cnx.commit()
    
    return redirect(url_for('customer_list'))


@webapp.route('/customer/create',methods=['GET'])
# Display an empty HTML form that allows users to define new customer.
def customer_create():
    return render_template("customer/new.html",title="New Customer")

@webapp.route('/customer/create',methods=['POST'])
# Create a new customer and save them in the database.
def customer_create_save():
    name = request.form.get('name',"")
    email = request.form.get('email',"")

    error = False

    if name == "" or email== "":
        error=True
        error_msg="Error: All fields are required!"
    
    if error:
        return render_template("customer/new.html",title="New Customer",error_msg=error_msg,
                               name=name, email=email)

    cnx = get_db()
    cursor = cnx.cursor()

    query = ''' INSERT INTO customer (name,email)
                       VALUES (%s,%s)
    '''

    cursor.execute(query,(name,email))
    cnx.commit()
    
    return redirect(url_for('customer_list'))



@webapp.route('/customer/delete/<int:id>',methods=['POST'])
# Deletes the specified customer from the database.
def customer_delete(id):
    cnx = get_db()
    cursor = cnx.cursor()

    query = "DELETE FROM customer WHERE id = %s"
    
    cursor.execute(query,(id,))
    cnx.commit()

    return redirect(url_for('customer_list'))


