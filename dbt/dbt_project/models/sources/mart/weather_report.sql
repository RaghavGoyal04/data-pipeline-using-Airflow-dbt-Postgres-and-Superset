{{
    config(
        materialized='table',
        unique_key='id'
    )
}}

select 
    city,
    main_weather,
    description,
    temperature,
    wind_speed,
    wind_direction,
    humidity,
    pressure,
    visibility,
    utc_offset,
    source_timestamp
from {{ ref('stg_weather_data') }}