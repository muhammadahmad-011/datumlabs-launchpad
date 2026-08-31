-- Full attacking-type x defending-type matrix, ready for a Hex heatmap.
-- Pairs not present in int_type_damage_relations_unnested are neutral (1x).

with all_pairs as (

    select
        a.type_name as attacking_type,
        d.type_name as defending_type
    from {{ ref('stg_type') }} a
    cross join {{ ref('stg_type') }} d

),

relations as (

    select * from {{ ref('int_type_damage_relations_unnested') }}

)

select
    p.attacking_type,
    p.defending_type,
    coalesce(r.multiplier, 1.0) as multiplier
from all_pairs p
left join relations r
    on p.attacking_type = r.attacking_type
   and p.defending_type = r.defending_type
