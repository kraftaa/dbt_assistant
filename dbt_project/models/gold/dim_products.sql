with transformed_data as (
    select
        product_id as product_id,
        product_name as product_name,
        category as category,
        price as price
    from {{ ref('stg_products') }}
    where price > 0
)   

select * from transformed_data
