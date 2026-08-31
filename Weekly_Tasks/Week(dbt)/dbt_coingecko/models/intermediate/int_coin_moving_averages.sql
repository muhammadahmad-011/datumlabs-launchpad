-- Rolling price averages and volatility (stddev of daily returns), the
-- building blocks for trend/risk signals in the marts layer.

with returns as (

    select * from {{ ref('int_coin_daily_returns') }}

),

windowed as (

    select
        coin_id,
        price_date,
        price_usd,
        daily_return_pct,

        avg(price_usd) over (
            partition by coin_id order by price_date
            rows between 6 preceding and current row
        ) as sma_7d_usd,

        avg(price_usd) over (
            partition by coin_id order by price_date
            rows between 29 preceding and current row
        ) as sma_30d_usd,

        stddev_samp(daily_return_pct) over (
            partition by coin_id order by price_date
            rows between 29 preceding and current row
        ) as volatility_30d,

        avg(volume_usd) over (
            partition by coin_id order by price_date
            rows between 6 preceding and current row
        ) as avg_volume_7d_usd

    from returns

)

select * from windowed
