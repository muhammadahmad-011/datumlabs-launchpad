select * from superstore_sales;

--A sales manager needs to query all orders above $500 without knowing the underlying table structure
--Create a regular view called vw_high_value_orders that shows all orders above $500. 
--Query it like a table and confirm it returns results

create view vw_high_value_orders
as
select order_id,category,sub_category,product_name,sales
from superstore_sales
where sales >= 5000;

select * from vw_high_value_orders

--Check what happens when the underlying data changes 
-- insert or update one row in the base table, then re-query the view. 
--Does it reflect the change automatically? Write a comment explaining what you observed

--comment--
--after insert and update row in a base table yes it's reflect the changes automatically because view is a 
--virtual table and fetch data from the base table so if i insert and update any thing in base table its 
--automaticaly changed

                            ------

--The BI team queries total revenue per category every morning and 
--it should not recalculate from scratch every time
--Create a materialized view called mv_revenue_by_category that shows total revenue per category

create materialized view mv_revenue_by_category
as
select category , sum(sales) as total_revenue
from superstore_sales
group by category;

select * from mv_revenue_by_category


--Insert a new row into the base table. Re-query the materialized view — observe that it does NOT reflect
--the change yet. Then run REFRESH MATERIALIZED VIEW mv_revenue_by_category and re-query.
--Write a comment explaining the difference in behaviour vs the regular view

insert into superstore_sales(row_id,order_id,order_date,ship_date,ship_mode,customer_id,
customer_name,segment,country,city,state,postal_code,region,product_id,category,sub_category,product_name,
sales,quantity,discount,profit)
values(9995,'CA-2014-119914','05-05-2014','10-05-2014','Second Class','CC-12220','Chris Cortes','Consumer',
'United States','Westminster','California','92683','West','OFF-AP-10002684','Office Supplies',
'Appliances','Acco 7-Outlet Masterpiece Power Center' ,5000,2,0,72.948)

refresh materialized view mv_revenue_by_category
select * from mv_revenue_by_category

--comment--
--(materialized view is physical cache that store result of query permanently in a disk as a table and this is not 
-- autmatically update untill refreshed query is run WHILE regular view is a virtual table that stores query and 
-- when select command is run its fetch data from base table).

                    -----

--Drop both the view and the materialized view cleanly using DROP VIEW and DROP MATERIALIZED VIEW

DROP VIEW vw_high_value_orders
DROP MATERIALIZED VIEW mv_revenue_by_category