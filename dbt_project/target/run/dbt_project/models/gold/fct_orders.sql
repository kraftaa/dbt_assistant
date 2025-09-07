
  
    

  create  table "postgres"."transform"."fct_orders__dbt_tmp"
  
  
    as
  
  (
    with transformed_data as (
    select
        order_id as order_id,
        customer_id as customer_id,
        order_date as order_date,
        total_amount as total_amount
    from "postgres"."transform"."stg_orders"
)

select * from transformed_data
  );
  