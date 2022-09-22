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


@webapp.route('/product', methods=['GET'])
# Display an HTML list of all product.
def product_list():
    # PART 2 Q3 Modify the code below so that the query also includes the category name for each product

    cnx = get_db()

    cursor = cnx.cursor()

    # your code start here
    query = ''' SELECT p.id, p.name, p.price, p.quantity
                FROM product p
            '''
    # your code ends here

    cursor.execute(query)

    return render_template("product/list.html", title="Product List", cursor=cursor)


@webapp.route('/product/edit/<int:id>', methods=['GET'])
# Display an editable HTML form populated with product data.
def product_edit(id):
    cnx = get_db()

    cursor = cnx.cursor()

    query = "SELECT * FROM product WHERE id = %s"

    cursor.execute(query, (id,))

    row = cursor.fetchone()

    id = row[0]
    name = row[1]
    price = row[2]
    quantity = row[3]
    category_id = row[4]

    query = "SELECT * FROM category"
    cursor.execute(query)

    return render_template("product/edit.html", title="Edit Course", id=id, name=name, price=price,
                           quantity=quantity, category_id=category_id, cursor=cursor)


@webapp.route('/product/edit/<int:id>', methods=['POST'])
# Save the form changes for a particular product to the database.
def product_edit_save(id):
    name = request.form.get('name', "")
    price = request.form.get('price', "")
    quantity = request.form.get('quantity', "")
    category_id = request.form.get('category_id', "")

    error = False

    if name == "" or quantity == "" or price == "" or category_id == "":
        error = True
        error_msg = "Error: All fields are required!"

    if error:
        return render_template("product/edit.html", title="New Course", error_msg=error_msg, id=id, name=name,
                               price=price, quantity=quantity, category_id=category_id)

    cnx = get_db()
    cursor = cnx.cursor()

    query = ''' UPDATE product SET name=%s, price=%s, quantity=%s, category_id=%s
                WHERE id = %s '''

    cursor.execute(query, (name, price, quantity, category_id, id))
    cnx.commit()

    return redirect(url_for('product_list'))


@webapp.route('/product/create', methods=['GET'])
# Display an empty HTML form that allows users to define new product.
def product_create():
    cnx = get_db()
    cursor = cnx.cursor()
    query = "SELECT * FROM category"
    cursor.execute(query)
    return render_template("product/new.html", title="New Product", cursor=cursor)


@webapp.route('/product/create', methods=['POST'])
# Create a new product and save them in the database.
def product_create_save():
    name = request.form.get('name', "")
    price = request.form.get('price', "")
    quantity = request.form.get('quantity', "")
    category_id = request.form.get('category_id', "")

    error = False

    if name == "" or price == "" or quantity == "" or category_id == "":
        error = True
        error_msg = "Error: All fields are required!"

    if error:
        return render_template("product/new.html", title="New Course", error_msg=error_msg, name=name,
                               price=price, quantity=quantity, category_id=category_id)

    cnx = get_db()
    cursor = cnx.cursor()

    query = ''' INSERT INTO product (name,price,quantity,category_id)
                       VALUES (%s,%s,%s,%s)
    '''

    cursor.execute(query, (name, price, quantity, category_id))
    cnx.commit()

    return redirect(url_for('product_list'))


@webapp.route('/product/delete/<int:id>', methods=['POST'])
# Deletes the specified product from the database.
def product_delete(id):
    cnx = get_db()
    cursor = cnx.cursor()

    query = "DELETE FROM product WHERE id = %s"

    cursor.execute(query, (id,))
    cnx.commit()

    return redirect(url_for('product_list'))


@webapp.route('/product/buy', methods=['POST'])
# Sell as product to a specific customer
def product_buy():
    customer_id = request.form.get('customer_id', "")
    product_id = request.form.get('product_id', "")

    if customer_id == "" or product_id == "":
        return "Error: All fields are required!"

    cnx = get_db()
    cursor = cnx.cursor()
    try:
        cnx.start_transaction()

        query = "SELECT quantity " \
                "FROM product where id = %s for update"

        cursor.execute(query, (product_id,))

        row = cursor.fetchone()

        quantity = int(row[0])

        if (quantity > 0):
            quantity -= 1

            query = "UPDATE product SET quantity = %s " \
                    "WHERE id = %s"
            cursor.execute(query, (quantity, product_id))

            query = "INSERT INTO customer_has_product (customer_id,product_id) " \
                    "VALUES (%s, %s)"
            cursor.execute(query, (customer_id, product_id))
            cnx.commit()
        else:
            return "Sold out"
            cnx.rollback()
    except:
        e = sys.exc_info()
        cnx.rollback()

    return redirect(url_for('customer_view', id=customer_id))
