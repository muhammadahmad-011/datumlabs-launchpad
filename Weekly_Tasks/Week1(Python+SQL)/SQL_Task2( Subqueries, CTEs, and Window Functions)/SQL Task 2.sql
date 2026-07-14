select * from superstore_sales;

                        --sub-query--

-- this query identified all individual sales that are more than the average sales of company
-- (it coudn't done in a single select bcz aggregate function cannot use in where clause and 
--  using a sub query allows to calculate avg sales of store then it compares value to each individual sales)
select * from superstore_sales
where sales >(select avg(sales) from superstore_sales);

-- this query find the profit margin by category of the store--
--(it cannot be in a single select bcz of aggregate inside an aggregate in this query)

select category, avg(profit_margin_subcat) as profit_margin_cat
from (select category,sum(profit / sales) * 100 as profit_margin_subcat
      from superstore_sales
	  group by category ) as summary
group by category;



                          --CTEs--

--CTEs is used here instead of a subquery for readability and reuseability that 
--separate inside query as a temporary table.

with avg_sales as (select avg(sales) as global_avg 
from superstore_sales 
)
select * from superstore_sales s
cross join avg_sales sa
where s.sales > sa.global_avg;

--chained CTEs is used here instead of a subqueries for readability and reuseability that 
--separate inside queries as a temporary tables.

WITH customer_performance AS (
    SELECT customer_id, customer_name, SUM(sales) as total_customer_sales
    FROM superstore_sales
    GROUP BY customer_id, customer_name),

overall_customer_average AS (
    SELECT AVG(total_customer_sales) as avg_spent_per_customer
    FROM customer_performance)

SELECT customer_name, total_customer_sales
FROM customer_performance cp, overall_customer_average oca
WHERE cp.total_customer_sales > oca.avg_spent_per_customer
ORDER BY cp.total_customer_sales DESC;

                    --Window Functions--
					
-- Write a query using ROW_NUMBER() or RANK() or DENSERANK() to rank rows within a group--


--ROW_NUMBER--
select 
	region,
	product_name,
	sales,
	ROW_NUMBER() OVER(PARTITION BY region order by sales desc) as row_num
from superstore_sales;


--RANK_NUMBER--
select 
	region,
	product_name,
	sales,
	RANK() OVER(PARTITION BY region order by sales desc) as row_num
from superstore_sales;

--DENSE_RANK--
select 
	region,
	product_name,
	sales,
	ROW_NUMBER() OVER(PARTITION BY region order by sales desc) as row_num
from superstore_sales;

-- Write a query using SUM() OVER() or AVG() OVER() to 
--calculate a running total or group average alongside each row--


--SUM() OVER()--
SELECT 
    order_id, 
    category, 
    sales,
    SUM(sales) OVER (PARTITION BY category) as avg_sales_Category
FROM superstore_sales;


--AVG() OVER()--
SELECT 
    order_id, 
    category, 
    sales,
    AVG(sales) OVER (PARTITION BY category) as avg_sales_Category
FROM superstore_sales;


-- Write a query using LAG() or LEAD() to compare each row to the previous or next row--

--LAG()--
SELECT 
    order_id, 
    order_date, 
    sales,
    LAG(sales) OVER (ORDER BY order_date::date) as previous_order_sales
FROM superstore_sales;

--LEAD()--
SELECT 
	order_id,
	order_date,
	sales,
	LEAD(sales) OVER(PARTITION BY order_date::date) as next_order_sales
from superstore_sales;

