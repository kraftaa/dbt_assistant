
      insert into "postgres"."transform"."int_customer_lifetime_value" ("customer_id", "lifetime_value")
    (
        select "customer_id", "lifetime_value"
        from "int_customer_lifetime_value__dbt_tmp090159722527"
    )


  