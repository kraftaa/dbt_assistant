

with transformed_data as (
select
    o.order_id as order_id,
    o.customer_id as customer_id,
    o.order_date as order_date,
    o.total_amount as total_amount,
    c.customer_name as customer_name
from "database_name"."transform"."stg_orders" o
join "database_name"."transform"."stg_customers" c
    on o.customer_id = c.customer_id


)

select * from transformed_data