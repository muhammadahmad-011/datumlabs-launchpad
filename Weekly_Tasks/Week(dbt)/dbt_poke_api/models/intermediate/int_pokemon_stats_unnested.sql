select
    p.pokemon_id,
    p.pokemon_name,
    stat_entry -> 'stat' ->> 'name'    as stat_name,
    (stat_entry ->> 'base_stat')::int  as base_stat,
    (stat_entry ->> 'effort')::int     as effort
from {{ ref('stg_pokemon') }} as p,
     unnest(cast(p.stats_json as json[])) as t(stat_entry)
