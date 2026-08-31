select
    p.pokemon_id,
    p.pokemon_name,
    ability_entry -> 'ability' ->> 'name'  as ability_name,
    (ability_entry ->> 'is_hidden')::boolean as is_hidden,
    (ability_entry ->> 'slot')::int          as slot
from {{ ref('stg_pokemon') }} as p,
     unnest(cast(p.abilities_json as json[])) as t(ability_entry)
