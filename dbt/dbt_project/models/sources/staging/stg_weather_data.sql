{{
    config(
        materialized='table',
        unique_key='id'
    )
}}

with source as (
    select * from {{ source('dev', 'raw_weather_data') }}
),
dedup as (
    select 
        id,
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
        to_timestamp(dt) AT TIME ZONE 'UTC' as  source_timestamp,
        inserted_at,
        row_number() over (partition by dt order by inserted_at desc) as rn
    from source
)

select 
    id,
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
    source_timestamp,
    inserted_at
from dedup
where rn = 1
order by inserted_at desc

