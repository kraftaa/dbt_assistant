
  create view "postgres"."transform"."stg_orders__dbt_tmp"
    
    
  as (
    

with transformed_data as (
    select 
        id as order_id,
        customer_id as customer_id,
        product_id as product_id,
        order_date as order_date,
        total_amount as total_amount
    from "postgres"."raw"."orders"
)

select * from transformed_data
  );