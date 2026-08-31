-- Business scenario: the core analytical fact table behind price/trend
-- dashboards and backtesting — one row per coin per day with returns,
-- moving averages, and volatility ready to chart or feed into a BI tool.

with returns as (

    select * from {{ ref('int_coin_daily_returns') }}

),

moving_avg as (

    select * from {{ ref('int_coin_moving_averages') }}

),

joined as (

    select
        r.coin_id,
        r.price_date,
        r.price_usd,
        r.market_cap_usd,
        r.volume_usd,
        r.daily_return_pct,
        r.return_7d_pct,
        m.sma_7d_usd,
        m.sma_30d_usd,
        m.volatility_30d,
        m.avg_volume_7d_usd,
        case
            when m.sma_7d_usd > m.sma_30d_usd then 'uptrend'
            when m.sma_7d_usd < m.sma_30d_usd then 'downtrend'
            else 'flat'
        end as trend_signal
    from returns r
    left join moving_avg m
        on r.coin_id = m.coin_id
        and r.price_date = m.price_date

)

select * from joined
