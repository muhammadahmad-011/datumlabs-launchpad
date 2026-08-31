with pokemon as (

    select * from {{ ref('stg_pokemon') }}

),

species as (

    select * from {{ ref('stg_pokemon_species') }}

),

types_pivoted as (

    select
        pokemon_id,
        max(case when type_slot = 1 then type_name end) as primary_type,
        max(case when type_slot = 2 then type_name end) as secondary_type
    from {{ ref('int_pokemon_types_unnested') }}
    group by pokemon_id

),

stats_totaled as (

    select
        pokemon_id,
        sum(base_stat) as total_base_stat
    from {{ ref('int_pokemon_stats_unnested') }}
    group by pokemon_id

)

select
    p.pokemon_id,
    p.pokemon_name,
    p.base_experience,
    p.height,
    p.weight,
    t.primary_type,
    t.secondary_type,
    s.total_base_stat,
    sp.is_legendary,
    sp.is_mythical,
    sp.is_baby,
    sp.capture_rate,
    sp.color,
    sp.habitat,
    sp.generation
from pokemon p
left join species sp        on p.species_name = sp.species_name
left join types_pivoted t   on p.pokemon_id = t.pokemon_id
left join stats_totaled s   on p.pokemon_id = s.pokemon_id
