{{ config(materialized='view') }}

with transformed_data as (
    select 
        id as product_id,
        product_name as product_name,
        category as category,
        price as price
    from {{ source('raw', 'products') }}
)

select * from transformed_data
