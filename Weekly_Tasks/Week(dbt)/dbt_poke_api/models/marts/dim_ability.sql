with ability as (

    select * from {{ ref('stg_ability') }}

),

english_effect as (

    select
        ability_id,
        entry ->> 'short_effect' as short_effect
    from ability,
         unnest(cast(effect_entries_json as json[])) as t(entry)
    where entry -> 'language' ->> 'name' = 'en'

)

select
    a.ability_id,
    a.ability_name,
    a.is_main_series,
    a.generation,
    e.short_effect
from ability a
left join english_effect e on a.ability_id = e.ability_id
