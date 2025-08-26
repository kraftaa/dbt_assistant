{{ config(materialized='view') }}

with transformed_data as (
    select 
        id as order_id,
        customer_id as customer_id,
        order_date as order_date,
        total_amount as total_amount
    from {{ source('raw', 'orders') }}
)

select * from transformed_data
