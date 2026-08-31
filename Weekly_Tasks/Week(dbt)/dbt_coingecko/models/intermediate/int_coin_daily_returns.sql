-- Day-over-day and 7-day return calculations per coin, used for volatility
-- and top-mover analysis downstream.

with history as (

    select * from {{ ref('stg_coingecko__history') }}

),

with_prior as (

    select
        coin_id,
        price_date,
        price_usd,
        market_cap_usd,
        volume_usd,
        lag(price_usd) over (partition by coin_id order by price_date)        as prior_day_price_usd,
        lag(price_usd, 7) over (partition by coin_id order by price_date)     as price_usd_7d_ago

    from history

),

calculated as (

    select
        coin_id,
        price_date,
        price_usd,
        market_cap_usd,
        volume_usd,
        prior_day_price_usd,
        price_usd_7d_ago,
        case when prior_day_price_usd > 0
             then (price_usd - prior_day_price_usd) / prior_day_price_usd
        end as daily_return_pct,
        case when price_usd_7d_ago > 0
             then (price_usd - price_usd_7d_ago) / price_usd_7d_ago
        end as return_7d_pct

    from with_prior

)

select * from calculated
