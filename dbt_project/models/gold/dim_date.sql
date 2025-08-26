with dates as (
    select generate_series(
        '2020-01-01'::date, 
        '2030-01-01'::date, 
        interval '1 day'
    ) as date_day
),

transformed_data as (
    select 
    date_day as date_day,
    extract(year from date_day) as year,
    extract(month from date_day) as month,
    extract(day from date_day) as day
    from dates
)
select * from transformed_data
