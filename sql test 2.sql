select * from olist_customers_dataset
select * from olist_order_items_dataset
select * from olist_order_payments_dataset
select * from olist_orders_dataset
select * from olist_products_dataset

--1. The slow monthly revenue report

select 
    DATE_TRUNC('month', o.order_purchase_timestamp)::DATE AS order_month,
    p.product_category_name,
    sum(oi.price) as total_revenue,
    count(distinct o.order_id) as total_orders
from olist_orders_dataset o
join olist_order_items_dataset oi on o.order_id = oi.order_id
join olist_products_dataset p on oi.product_id = p.product_id
where o.order_status = 'delivered'
group by 1, 2
order by order_month desc, total_revenue desc;

--2. Spot the subquery trap

with avg_payments_by_type as (
    	select 
        payment_type, 
        avg(payment_value) as avg_payment_val
	    from olist_order_payments_dataset
    	group by payment_type)
select 
    o.order_id, 
    o.customer_id, 
    p.payment_value, 
    p.payment_type
from olist_orders_dataset o
join olist_order_payments_dataset p ON o.order_id = p.order_id
join avg_payments_by_type ap ON p.payment_type = ap.payment_type
where p.payment_value > ap.avg_payment_val;


--3. Late deliveries — window function vs. self-join

with order_delivery_durations as (
    select
        o.order_id,
        c.customer_state,
        o.order_delivered_customer_date::DATE as delivery_date,
        (o.order_delivered_customer_date - o.order_purchase_timestamp) as delivery_duration,
        lag(o.order_delivered_customer_date - o.order_purchase_timestamp) over(
            partition by c.customer_state, o.order_delivered_customer_date::DATE
            order by o.order_delivered_customer_date asc) as previous_delivery_duration
    from olist_orders_dataset o
    join olist_customers_dataset c on o.customer_id = c.customer_id
    where o.order_status = 'delivered' and o.order_delivered_customer_date is not null
      		AND o.order_purchase_timestamp IS NOT NULL)
select 
    order_id,
    customer_state,
    delivery_date,
    delivery_duration,
    previous_delivery_duration
from order_delivery_durations
where delivery_duration > previous_delivery_duration;

--4.The UNION anti-pattern

with combined_payments as (
    select p.order_id, p.payment_type 
    from olist_order_payments_dataset p
    join olist_orders_dataset o on p.order_id = o.order_id
    where p.payment_type = 'credit_card'
      and o.order_purchase_timestamp >= '2018-01-01' 
      and o.order_purchase_timestamp < '2019-01-01'
    
    union all
    
    select p.order_id, p.payment_type 
    from olist_order_payments_dataset p
    join olist_orders_dataset o ON p.order_id = o.order_id
    where p.payment_type = 'boleto'
      and o.order_purchase_timestamp >= '2018-01-01' 
      and o.order_purchase_timestamp < '2019-01-01')
select 
    payment_type, 
    count(order_id) as total_orders
from combined_payments
group by payment_type;


--5.Build the pre-aggregated summary table

create table monthly_category_revenue (
    reporting_month date not null,
    product_category_name varchar(100) not null,
    total_revenue numeric(14, 2) not null default 0,
    total_orders int not null default 0,
    avg_freight numeric(10, 2) not null default 0,
    primary key (reporting_month, product_category_name));

CREATE INDEX idx_monthly_cat_rev_perf 
ON monthly_category_revenue (reporting_month, total_revenue DESC);


