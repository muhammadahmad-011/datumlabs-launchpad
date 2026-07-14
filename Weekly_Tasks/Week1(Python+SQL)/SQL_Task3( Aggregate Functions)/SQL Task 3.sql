select * from superstore_sales;

--How many total orders were placed in this dataset?
--(count() returns the total number of rows including nulls while count(column_name) returns the rows excluding nulls)

select count(*)
from superstore_sales;

select count(postal_Code) as total_postal_codes
from superstore_sales;

--What is the total revenue across all orders?
--Write a query using SUM() to answer this

select sum(sales) as total_revenue
from superstore_sales;

--What is the average order value?
--Write a query using AVG() to answer this. Use ROUND() to limit the result to 2 decimal places

select ROUND(avg(sales),2) as avg_order_sales
from superstore_sales;

--What are the earliest and latest order dates in the dataset?
--Write a query using both MIN() and MAX() on your date column in the same query

select 
	min(order_date) as earliest_date,
	max(order_date) as latest_date
from superstore_sales;

--What is the total revenue broken down by both region and product category?
--Write a query using GROUP BY on two columns — not just one

select region , category ,sum(sales) as total_revenue
from superstore_sales
group by region , category
order by category;

--Which product categories generated more than $10,000 in total revenue?
--Write a query using GROUP BY + HAVING to filter aggregated results above the threshold

select category , sum(sales) as total_revenue
from superstore_sales
group by category
having sum(sales) > 800000;

--Which categories are above the average total revenue across all categories?
--Write a query using a CTE to calculate total revenue per category first, 
--then filter in the outer query to only show categories above the overall average

with total_revenue_category as (
			select category, sum(sales) as total_revenue
			from superstore_sales
			group by category),

		avg_revenue_category as (select avg(total_revenue) as avg_revenue
								from total_revenue_category)

select *
from total_revenue_category as trc
cross join avg_revenue_category as arc
where trc.total_revenue > arc.avg_revenue;


--What is the average order value per region, rounded to 2 decimal places?
--Write a query using AVG() + ROUND() grouped by region

select region , round(avg(sales),2)
from superstore_sales
group by region;


--Look up COUNT(DISTINCT column) — how is it different from COUNT(column)? Write a query using it --
--(select count(distinct) only return unique value from data and ignores null value WHILE count() return all the number of rows)

select count(distinct category)
from superstore_sales;
