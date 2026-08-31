with source as (

    select * from {{ source('raw_pokemon', 'pokemon_species') }}

)

select
    id                                  as species_id,
    name                                as species_name,
    gender_rate,
    capture_rate,
    base_happiness,
    is_baby,
    is_legendary,
    is_mythical,
    hatch_counter,
    growth_rate ->> 'name'              as growth_rate,
    color ->> 'name'                    as color,
    shape ->> 'name'                    as shape,
    habitat ->> 'name'                  as habitat,
    generation ->> 'name'               as generation,
    evolves_from_species ->> 'name'     as evolves_from_species,
    varieties                           as varieties_json,
    _dlt_load_id,
    _dlt_id
from source
