{{
    config(
        materialized='table',
        unique_key='id'
    )
}}

select 
    city,
    date(source_timestamp) as report_date,
    round(avg(temperature)::numeric, 2) as avg_temperature,
    round(avg(wind_speed)::numeric, 2) as avg_wind_speed,
    round(avg(humidity)::numeric, 2) as avg_humidity,
    round(avg(pressure)::numeric, 2) as avg_pressure,
    round(avg(visibility)::numeric, 2) as avg_visibility,
    min(source_timestamp) as first_report_time,
    max(source_timestamp) as last_report_time
from {{ ref('stg_weather_data') }}
where source_timestamp >= current_date - interval '30 days'
group by city, date(source_timestamp)
order by city, report_date