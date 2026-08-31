with source as (

    select * from {{ source('coingecko_data', 'history') }}

),

renamed as (

    select
        coin_id,
        cast(date as date)              as price_date,
        cast(date_ts as bigint)         as price_date_ts,
        cast(price_usd as double)       as price_usd,
        cast(market_cap_usd as double)  as market_cap_usd,
        cast(volume_usd as double)      as volume_usd,
        _dlt_load_id                    as dlt_load_id

    from source
    where coin_id is not null
      and date is not null

)

select * from renamed
