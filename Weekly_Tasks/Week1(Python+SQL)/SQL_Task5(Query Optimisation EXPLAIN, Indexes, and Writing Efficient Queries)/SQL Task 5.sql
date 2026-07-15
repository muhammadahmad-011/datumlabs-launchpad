--take one of your more complex queries from Task 1 or 2 and run EXPLAIN ANALYZE on it 
--find the most expensive step (look for high cost numbers or sequential scans)

--find average total sales per customer and show only those customer who spent more than average sales

EXPLAIN ANALYZE
WITH customer_performance AS (
    SELECT customer_id, customer_name , SUM(sales) as total_customer_sales
    FROM superstore_sales
	group by customer_id, customer_name),

overall_customer_average AS (
    SELECT AVG(total_customer_sales) as avg_spent_per_customer
    FROM customer_performance)

SELECT * , total_customer_sales
FROM superstore_sales
cross join customer_performance cp, overall_customer_average oca
WHERE cp.total_customer_sales > oca.avg_spent_per_customer
ORDER BY cp.total_customer_sales DESC;
--high cost = Nested Loop  (cost=22.48..42075.76)
--Seq Scan = superstore_sales (cost=0.00..419.94)

                                    ------

--Rewrite the same query to avoid SELECT * — select only the columns you actually need. 
--Run EXPLAIN ANALYZE again and compare

EXPLAIN ANALYZE
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

--high cost = HashAggregate  (cost=494.89..507.38
--Seq Scan = Seq Scan on superstore_sales  (cost=0.00..419.94)

                                      -----


--Create an index on a column you frequently filter or join on. 
--Run the query again and compare the execution plan before and after

CREATE INDEX idx_customer_id ON superstore_sales(customer_id);

EXPLAIN ANALYZE
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

--(in comparison with execution plan before and after nothing change bcz the current table has only 9995 rows and
-- for database these table is just like 4 to 5 pages rather than whole book)

                                        -----

--Take one of your subquery-based queries and rewrite it as a CTE. 
--Compare readability and performance using EXPLAIN ANALYZE


                          -- sub-query based --
explain analyze
select * from superstore_sales
where sales >(select avg(sales) as avg_sales from superstore_sales);


                             --CTEs based --
explain analyze
with average_sales as (select avg(sales) as avg_sales from superstore_sales)
select * from superstore_sales sp
cross join average_sales s
where sp.sales > s.avg_sales;

--(readability of CTEs is better than sub-query bcz in sub-query there is query inside another query WHILE in CTEs the 
-- temporary table created before main query and fetch details through the name of created CTEs temporary table so its easy to read.)
--(and perfomance of sub-query in this dataset better than CTEs bcz data is lower than 10000 rows while in larger dataset CTEs give better perfomance)
--Execution Time: 9.343 ms (sub-query based)
--Execution Time: 14.182 ms (CTEs based)

                                        -----


--Write a deliberately inefficient query (SELECT * on a large table, no WHERE clause) then write the optimised version side by side


--deliberately inefficient query--

select * from superstore_sales;


--optimised version--

select category , sub_category , sum(sales) as total_sales
from superstore_sales
where sales > 500
group by category , sub_category
having category = 'Office Supplies'
order by total_sales desc
limit 5;


--Look up what a sequential scan vs an index scan means in an execution plan. When does adding an index actually
--make things slower instead of faster? Write a comment in your file explaining what you found

--(sequential scan read database everysingle row from start to end while index is like a customer id that i can access directly without go through all the data
-- and adding index make things faster to fetch)

