
      insert into "postgres"."transform"."int_order_product_count" ("order_id", "product_count")
    (
        select "order_id", "product_count"
        from "int_order_product_count__dbt_tmp090159790485"
    )


  