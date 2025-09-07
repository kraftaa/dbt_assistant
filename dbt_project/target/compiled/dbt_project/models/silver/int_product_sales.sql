

with transformed_data as (
select
    o.order_id as order_id,
    p.product_id as product_id,
    p.product_name as product_name,
    p.category as category,
    o.total_amount as total_amount
from "postgres"."transform"."stg_orders" o
join "postgres"."transform"."stg_products" p
    on true  -- placeholder join


  -- Only bring in orders newer than what we've already processed
  where o.order_date > (select max(order_date) from "postgres"."transform"."int_product_sales")

)

select * from transformed_data