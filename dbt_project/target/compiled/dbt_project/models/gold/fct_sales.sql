with transformed_data as (
    select
        order_id as order_id,
        product_id as product_id,
        total_amount as sales_amount
    from "database_name"."transform"."int_product_sales"
)

select * from transformed_data