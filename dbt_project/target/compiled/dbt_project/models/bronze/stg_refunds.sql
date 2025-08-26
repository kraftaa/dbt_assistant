-- bronze/stg_refunds.sql

with transformed_data as (
    select 
        id as refund_id,
        order_id as order_id,
        customer_id as customer_id,
        refund_date as refund_date,
        refund_amount as refund_amount
    from "sci_rx_production"."raw"."refunds"
)
select * from transformed_data