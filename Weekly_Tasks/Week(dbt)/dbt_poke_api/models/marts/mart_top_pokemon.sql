select
    pokemon_id,
    pokemon_name,
    primary_type,
    secondary_type,
    total_base_stat,
    is_legendary,
    is_mythical,
    rank() over (order by total_base_stat desc) as power_rank
from {{ ref('dim_pokemon') }}
order by total_base_stat desc
