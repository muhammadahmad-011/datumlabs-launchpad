-- Business scenario: an executive/market-wide summary — total tracked
-- market cap, BTC/ETH dominance, and breadth (advancing vs declining coins)
-- for a single "market health" chart, one row per day.

with daily_metrics as (

    select * from {{ ref('fct_coin_daily_metrics') }}

),

daily_totals as (

    select
        price_date,
        sum(market_cap_usd)                                            as total_market_cap_usd,
        sum(volume_usd)                                                as total_volume_usd,
        count(distinct coin_id)                                        as coins_tracked,
        count(distinct case when daily_return_pct > 0 then coin_id end) as coins_advancing,
        count(distinct case when daily_return_pct < 0 then coin_id end) as coins_declining
    from daily_metrics
    group by price_date

),

dominance as (

    select
        price_date,
        sum(case when coin_id = 'bitcoin'  then market_cap_usd else 0 end) as btc_market_cap_usd,
        sum(case when coin_id = 'ethereum' then market_cap_usd else 0 end) as eth_market_cap_usd
    from daily_metrics
    group by price_date

)

select
    t.price_date,
    t.total_market_cap_usd,
    t.total_volume_usd,
    t.coins_tracked,
    t.coins_advancing,
    t.coins_declining,
    d.btc_market_cap_usd,
    d.eth_market_cap_usd,
    case when t.total_market_cap_usd > 0
         then d.btc_market_cap_usd / t.total_market_cap_usd
    end as btc_dominance_pct,
    case when t.total_market_cap_usd > 0
         then d.eth_market_cap_usd / t.total_market_cap_usd
    end as eth_dominance_pct
from daily_totals t
left join dominance d on t.price_date = d.price_date
