with transformed_data as (
    select distinct
        customer_id as customer_id,
        customer_name as customer_name,
        email as email
    from "sci_rx_production"."transform"."stg_customers"
)

select * from transformed_data