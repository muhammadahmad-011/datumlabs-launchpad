with source as (

    select * from {{ source('raw_pokemon', 'pokemon') }}

)

select
    id                  as pokemon_id,
    name                as pokemon_name,
    base_experience,
    height,
    weight,
    is_default,
    "order"             as pokemon_order,
    species ->> 'name'  as species_name,
    types               as types_json,
    stats               as stats_json,
    abilities           as abilities_json,
    _dlt_load_id,
    _dlt_id
from source
