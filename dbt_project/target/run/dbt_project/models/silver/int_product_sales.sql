
      
        
        
        delete from "postgres"."transform"."int_product_sales" as DBT_INTERNAL_DEST
        where (order_id) in (
            select distinct order_id
            from "int_product_sales__dbt_tmp090159658460" as DBT_INTERNAL_SOURCE
        );

    

    insert into "postgres"."transform"."int_product_sales" ("order_id", "product_id", "product_name", "category", "total_amount", "order_date")
    (
        select "order_id", "product_id", "product_name", "category", "total_amount", "order_date"
        from "int_product_sales__dbt_tmp090159658460"
    )
  