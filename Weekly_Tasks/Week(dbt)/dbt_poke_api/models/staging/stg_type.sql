with source as (

    select * from {{ source('raw_pokemon', 'type') }}

)

select
    id                          as type_id,
    name                        as type_name,
    damage_relations            as damage_relations_json,
    generation ->> 'name'       as generation,
    _dlt_load_id,
    _dlt_id
from source
