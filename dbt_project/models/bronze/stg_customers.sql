{{ config(materialized='view') }}

with transformed_data as (
    select 
        id as customer_id,
        name as customer_name,
        email as email,
        created_at as created_at
    from {{ source('raw', 'customers') }}
) 

select * from transformed_data
