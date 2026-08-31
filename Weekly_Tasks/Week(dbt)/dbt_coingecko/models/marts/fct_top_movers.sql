-- Business scenario: "top gainers / losers today" — the feed behind a
-- trading desk watchlist or a daily digest alert.
-- Materialized as a view: this is a reshape/filter of fct_coin_daily_metrics,
-- not new data, so a table would just duplicate storage.

{{ config(materialized='view') }}

with daily_metrics as (

    select * from {{ ref('fct_coin_daily_metrics') }}

),

coins as (

    select coin_id, coin_symbol, coin_name, market_cap_tier from {{ ref('dim_coins') }}

),

latest_day as (

    select max(price_date) as max_date from daily_metrics

),

ranked as (

    select
        d.coin_id,
        c.coin_symbol,
        c.coin_name,
        c.market_cap_tier,
        d.price_date,
        d.price_usd,
        d.daily_return_pct,
        d.volume_usd,
        rank() over (order by d.daily_return_pct desc) as gain_rank,
        rank() over (order by d.daily_return_pct asc)  as loss_rank
    from daily_metrics d
    inner join latest_day l on d.price_date = l.max_date
    left join coins c on d.coin_id = c.coin_id
    where d.daily_return_pct is not null

)

select
    coin_id,
    coin_symbol,
    coin_name,
    market_cap_tier,
    price_date,
    price_usd,
    daily_return_pct,
    volume_usd,
    gain_rank,
    loss_rank,
    case
        when gain_rank <= 10 then true else false
    end as is_top_10_gainer,
    case
        when loss_rank <= 10 then true else false
    end as is_top_10_loser
from ranked
