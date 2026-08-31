with source as (

    select * from {{ source('coingecko_data', 'markets') }}

),

renamed as (

    select
        id                                      as coin_id,
        symbol                                   as coin_symbol,
        name                                      as coin_name,
        -- dlt splits some numeric fields into a nullable base column plus a
        -- "__v_double" variant when CoinGecko's API returned mixed types.
        -- Coalescing means downstream models always get a numeric value.
        coalesce(cast(current_price as double), current_price__v_double)         as current_price_usd,
        cast(market_cap as double)                as market_cap_usd,
        market_cap_rank,
        coalesce(cast(total_volume as double), total_volume__v_double)           as total_volume_usd,
        coalesce(cast(high_24h as double), high_24h__v_double)                   as high_24h_usd,
        coalesce(cast(low_24h as double), low_24h__v_double)                     as low_24h_usd,
        cast(price_change_24h as double)          as price_change_24h_usd,
        cast(price_change_percentage_24h as double)      as price_change_pct_24h,
        coalesce(cast(market_cap_change_24h as double), market_cap_change_24h__v_double) as market_cap_change_24h_usd,
        cast(market_cap_change_percentage_24h as double) as market_cap_change_pct_24h,
        cast(circulating_supply as double)        as circulating_supply,
        cast(total_supply as double)              as total_supply,
        cast(max_supply as double)                as max_supply,
        coalesce(cast(ath as double), ath__v_double)                            as ath_usd,
        cast(ath_change_percentage as double)     as ath_change_pct,
        cast(ath_date as timestamp)               as ath_date,
        cast(atl as double)                       as atl_usd,
        cast(atl_change_percentage as double)     as atl_change_pct,
        cast(atl_date as timestamp)               as atl_date,
        cast(last_updated as timestamp)           as last_updated_at,
        _dlt_load_id                              as dlt_load_id

    from source
    where id is not null

)

select * from renamed
