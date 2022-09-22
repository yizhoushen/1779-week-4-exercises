
#get the id and name of all categories
select * from category;					

#get the names of all the video games
select name from product where category_id = 1; 	 

#get the category name for the product with id=3
select c.name 										
from product as p join category as c on p.category_id = c.id 
where p.id = 3;

#for all customers, get the names of all the products they own
select c.name as "Customer Name", p.name as "Product Name" 
from product as p 
join customer_has_product as cp 
join customer as c 
on p.id = cp.product_id and 
   cp.customer_id = c.id;

# create a new category for songs
insert into category (name) values ('Songs');		



