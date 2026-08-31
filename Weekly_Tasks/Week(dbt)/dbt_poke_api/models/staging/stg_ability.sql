with source as (

    select * from {{ source('raw_pokemon', 'ability') }}

)

select
    id                          as ability_id,
    name                        as ability_name,
    is_main_series,
    generation ->> 'name'       as generation,
    effect_entries               as effect_entries_json,
    _dlt_load_id,
    _dlt_id
from source
