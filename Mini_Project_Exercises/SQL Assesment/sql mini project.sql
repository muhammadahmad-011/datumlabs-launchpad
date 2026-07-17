select * from superstore_sales

--1. avg total revenue generated region--

with revenue as (select region,sum(sales) as total_state_sales
    					from superstore_sales
    					group by region)
select region,ROUND(avg(total_state_sales)) as avg_revenue
from revenue
group by region
order by avg_revenue desc;

                                   ---------------

--2. find top 10 customer based on highest sales--

select row_id ,customer_id , customer_name, state , sum(sales)
from superstore_sales
group by row_id ,customer_id , customer_name, state 
order by sum(sales) desc
limit 10;

                                   ---------------

--3. which category has sell more in each state

select
	state, 
	category, 
	round(sum(sales)) as total_sales,
	row_number() over(partition by state order by round(sum(sales)) desc ) as row_num
from superstore_sales
group by state , category
order by state asc , total_sales desc;
   
									 ---------

--4. find average order value 

with orders_calculation as (select count(distinct(order_id)) as total_order , sum(sales) as total_sales
							from superstore_sales)

select round(avg(total_sales/total_order),2) as avg_order_value
from superstore_sales
cross join orders_calculation o ;

                                       --------

--5. find avg profit margin by category

select 
    category,
    round((sum(profit) / sum(sales)) * 100, 2) as avg_profit_margin
from superstore_sales
group by category
order by avg_profit_margin DESC;
                                             
											-------

--6. which ship mode is most used and have more revenue

select ship_mode , count(order_id) as total_order , round(sum(sales)) as total_revenue
from superstore_sales
group by ship_mode
order by total_revenue desc;
                                         
										 ---------

--7. which segment has more order and sales
select 
	segment ,
	count(order_id) as total_order ,
	sum(sales) as total_sales,
	row_number() over(partition by segment) as row_num
from superstore_sales
group by segment

                                         --------
								 
--8. top performing city by states which has highest revenue

with calculation as (select 
			state , 
			city , 
			sum(sales) as total_revenue,
	        rank() over(partition by state order by sum(sales) desc) as rank
			from superstore_sales
			group by state , city)

select state, city ,total_revenue
from calculation
where rank = 1;
						