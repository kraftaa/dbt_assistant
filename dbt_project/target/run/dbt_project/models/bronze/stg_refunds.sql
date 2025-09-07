
  create view "postgres"."transform"."stg_refunds__dbt_tmp"
    
    
  as (
    -- bronze/stg_refunds.sql

with transformed_data as (
    select 
        id as refund_id,
        order_id as order_id,
        customer_id as customer_id,
        refund_date as refund_date,
        refund_amount as refund_amount
    from "postgres"."raw"."refunds"
)
select * from transformed_data
  );