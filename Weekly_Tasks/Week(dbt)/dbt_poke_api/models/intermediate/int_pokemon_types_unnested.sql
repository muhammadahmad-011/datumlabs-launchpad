select
    p.pokemon_id,
    p.pokemon_name,
    (type_entry ->> 'slot')::int    as type_slot,
    type_entry -> 'type' ->> 'name' as type_name
from {{ ref('stg_pokemon') }} as p,
     unnest(cast(p.types_json as json[])) as t(type_entry)
