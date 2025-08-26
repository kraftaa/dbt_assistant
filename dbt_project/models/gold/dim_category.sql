-- gold/dim_category.sql
with transformed_data as (
    select
        category as category,
        count(product_id) as product_count
    from {{ ref('stg_products') }}
    group by category
)
select * from transformed_data
