-- Business scenario: a single reference dimension analysts/BI tools join
-- against — current attributes plus a market-cap tier classification used
-- across risk and portfolio-construction reporting.

with markets as (

    select * from {{ ref('stg_coingecko__markets') }}

),

classified as (

    select
        coin_id,
        coin_symbol,
        coin_name,
        current_price_usd,
        market_cap_usd,
        market_cap_rank,
        total_volume_usd,
        circulating_supply,
        total_supply,
        max_supply,
        ath_usd,
        ath_change_pct,
        ath_date,
        atl_usd,
        atl_change_pct,
        atl_date,
        case
            when market_cap_usd >= 10000000000 then 'large_cap'
            when market_cap_usd >= 1000000000  then 'mid_cap'
            when market_cap_usd >= 100000000   then 'small_cap'
            else 'micro_cap'
        end as market_cap_tier,
        case
            when max_supply is not null and max_supply > 0
            then circulating_supply / max_supply
        end as supply_issued_pct,
        last_updated_at
    from markets

)

select * from classified
