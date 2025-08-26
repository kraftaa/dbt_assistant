

with transformed_data as (
select
    o.order_id as order_id,
    p.product_id as product_id,
    p.product_name as product_name,
    p.category as category,
    o.total_amount as total_amount
from "sci_rx_production"."transform"."stg_orders" o
join "sci_rx_production"."transform"."stg_products" p
    on true  -- placeholder join


)

select * from transformed_data