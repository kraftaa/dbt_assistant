
      
        
        
        delete from "postgres"."transform"."int_customer_orders" as DBT_INTERNAL_DEST
        where (order_id) in (
            select distinct order_id
            from "int_customer_orders__dbt_tmp090159539047" as DBT_INTERNAL_SOURCE
        );

    

    insert into "postgres"."transform"."int_customer_orders" ("order_id", "customer_id", "order_date", "total_amount", "customer_name")
    (
        select "order_id", "customer_id", "order_date", "total_amount", "customer_name"
        from "int_customer_orders__dbt_tmp090159539047"
    )
  