{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

with transformed_data as (
select
    o.order_id as order_id,
    o.customer_id as customer_id,
    o.order_date as order_date,
    o.total_amount as total_amount,
    c.customer_name as customer_name
from {{ ref('stg_orders') }} o
join {{ ref('stg_customers') }} c
    on o.customer_id = c.customer_id

{% if is_incremental() %}
  -- Only bring in new/updated orders
  where o.order_date > (select max(order_date) from {{ this }})
{% endif %}
)

select * from transformed_data