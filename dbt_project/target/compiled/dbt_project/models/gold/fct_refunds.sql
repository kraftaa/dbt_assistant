-- gold/fct_refunds.sql
with transformed_data as (
    select
        refund_id as refund_id,
        order_id as order_id,
        customer_id as customer_id,
        refund_date as refund_date,
        refund_amount as refund_amount
    from "database_name"."transform"."stg_refunds"
)
select * from transformed_data