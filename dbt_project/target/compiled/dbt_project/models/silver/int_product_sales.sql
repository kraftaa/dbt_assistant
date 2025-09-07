

with transformed_data as (
    select
        o.order_id,
        o.product_id,
        p.product_name,
        p.category,
        o.total_amount,
        o.order_date
    from "postgres"."transform"."stg_orders" o
    join "postgres"."transform"."stg_products" p on o.product_id = p.product_id
    WHERE 1=1
    
        AND order_date > coalesce((select max(order_date) from "postgres"."transform"."int_product_sales"), '1900-01-01'::timestamp)
    
)

select * from transformed_data