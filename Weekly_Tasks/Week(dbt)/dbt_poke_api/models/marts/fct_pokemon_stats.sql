select
    pokemon_id,
    pokemon_name,
    stat_name,
    base_stat,
    effort
from {{ ref('int_pokemon_stats_unnested') }}
