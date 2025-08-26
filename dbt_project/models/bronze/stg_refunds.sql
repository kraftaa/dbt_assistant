-- bronze/stg_refunds.sql
{{ config(materialized='view') }}
with transformed_data as (
    select 
        id as refund_id,
        order_id as order_id,
        customer_id as customer_id,
        refund_date as refund_date,
        refund_amount as refund_amount
    from {{ source('raw', 'refunds') }}
)
select * from transformed_data
