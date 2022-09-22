from flask import render_template, redirect, url_for, request, g
from app import webapp

import mysql.connector

from app.config import db_config

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

@webapp.route('/category',methods=['GET'])
# Display an HTML list of all categories.
def category_list():
    # PART 2 Q1 complete this function by creating a cursor that returns all
    # column for all tuples in the category table.

    cnx = get_db()          # get a database connection

    cursor = cnx.cursor()   # create a database cursor

    
    
    ## your code starts here
    # See W3 schools for how to write a select statement: https://www.w3schools.com/sql/sql_select.asp
    # The offical MySQl documentation for the Select statement feature can be found here: https://dev.mysql.com/doc/refman/8.0/en/select.html
    # Tip: start with the W3 schools website first because it is simpler as it has enough information for you to compelte this task.

    query = '''SELECT '''

    ## your code ends here

    cursor.execute(query)


    return render_template("category/list.html",title="Category List", cursor=cursor)


@webapp.route('/category/create',methods=['GET'])
# Display an empty HTML form that allows users to define new student.
def category_create():
    return render_template("category/new.html",title="New Category")

@webapp.route('/category/create',methods=['POST'])
# Create a new student and save them in the database.
def category_create_save():
    # PART 2 Q2 add new category to database.   This function will be invoked when the user
    # submits the form created by category_create() above


    name = request.form.get('name',"")      # get new name from parameter in form

    cnx = get_db()                          # get database connection
    cursor = cnx.cursor()                   # create cursor

    
    # See W3 schools for how to write an Insert statement: https://www.w3schools.com/sql/sql_insert.asp
    # The offical MySQl documentation for the Insert statement feature can be found here: https://dev.mysql.com/doc/refman/8.0/en/insert.html
    ## your code start here

    query = '''INSERT INTO '''

    ## your code ends here

    cursor.execute(query,(name,))    


    cnx.commit()                            # commit changes

    return redirect(url_for('category_list'))



@webapp.route('/category/delete/<int:id>',methods=['POST'])
# Deletes the specified student from the database.
def category_delete(id):
    cnx = get_db()
    cursor = cnx.cursor()

    query = "DELETE FROM category WHERE id = %s"

    cursor.execute(query,(id,))
    cnx.commit()

    return redirect(url_for('category_list'))

