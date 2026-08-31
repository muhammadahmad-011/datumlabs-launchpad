-- Flattens each type's damage_relations JSON into
-- (attacking_type, defending_type, multiplier) rows.
-- Only non-1x relations exist in the source; 1x (neutral) pairs are
-- filled in later in mart_type_matchups.

with base as (

    select type_name, damage_relations_json
    from {{ ref('stg_type') }}

),

double_to as (
    select
        type_name           as attacking_type,
        entry ->> 'name'     as defending_type,
        2.0                  as multiplier
    from base,
         unnest(cast(damage_relations_json -> 'double_damage_to' as json[])) as t(entry)
),

half_to as (
    select
        type_name           as attacking_type,
        entry ->> 'name'     as defending_type,
        0.5                  as multiplier
    from base,
         unnest(cast(damage_relations_json -> 'half_damage_to' as json[])) as t(entry)
),

no_to as (
    select
        type_name           as attacking_type,
        entry ->> 'name'     as defending_type,
        0.0                  as multiplier
    from base,
         unnest(cast(damage_relations_json -> 'no_damage_to' as json[])) as t(entry)
)

select * from double_to
union all
select * from half_to
union all
select * from no_to
