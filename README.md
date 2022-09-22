
# Week 4 Exercises
The following exercises are intended to help familiarize you with SQL databases and queries. This week's exercises will also count towards your participation mark; please follow the instructions below.

## Part 1: Complete the following exercises using the Part1 folder:


You will use the terminal and the command line tool mysql to execute SQL
queries on the estore database. Open the file estore_diagram.png to see an
entity-relationship diagram of the database. The file example_queries.txt
contains some example queries.

Resources to help with this task:

- https://www.w3schools.com/sql/sql_select.asp
- https://www.w3schools.com/sql/sql_join_inner.asp
- https://www.w3schools.com/sql/sql_where.asp

### Set Up Instructions:

Install mysql onto your machine.

Start your SQL server
``` $ mysql.server start ```

Start mysql
``` $ mysql -u root -p ```

``` source estore.sql;```
``` use estore; ```

### Exercises:

1. Write a query that returns all information for the customer with id = 2.
You can use the following code as a starting point:
```
   SELECT *
   FROM estore.customer;
```
   
Enter the name of the above customer on [PCRS](https://pcrs.teach.cs.toronto.edu/ECE1779-2022-09/content/quests) by completing the question on
the Week4: Perform section.


2. Write a query that returns only the name and the quantity of available items
for all products that cost between 15 and 20.  You can use the following code
as a starting point:
```
   SELECT *
   FROM estore.product;
```

3. Write a query that returns the names of all products and the name of their
category.  You can use the following code
as a starting point:
```
   SELECT p.name as "Product Name", c.name as "Category Name"
   FROM estore.product as p join estore.category c;
```

## Part 2: Complete the following exercises in the Part2 folder:

### Set Up Instructions:

You will once again be running a flask app locally on your machine, so all set-up from Week 3's exercises applies to this week as well. 
In addition to the flask app set-up, make sure that you have:

- Connector/Python installed
(https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)
- Your SQL server running.

Then run the flask application. 
Note: your app will be running on http://[your-pirvate-ip]:5000

### Exercises: 

1) Add the necessary code to the function category_list located in the file
app/category.py so that it display all the data in the category table.

2) Add the necessary code to the function category_create_save located in
the file app/category.py so that it insert a new record to the category table.

3) Modify the query in the function product_list in the file app/product.py so
that it the result also includes the category name for each product.

#### Important: remember to stop and restart the run.py whenever you make a change to the code. The flask server needs to reload the code everytime a change is made.



