-- silver/int_order_product_count.sql
with transformed_data as (
    select
        order_id as order_id,
        count(product_id) as product_count
    from {{ ref('int_product_sales') }}
    group by order_id
)
select * from transformed_data
