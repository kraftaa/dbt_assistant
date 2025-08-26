-- silver/int_customer_lifetime_value.sql
with transformed_data as (
    select
        customer_id as customer_id,
        sum(total_amount) as lifetime_value
    from "database_name"."transform"."int_customer_orders"
    group by customer_id
)
select * from transformed_data