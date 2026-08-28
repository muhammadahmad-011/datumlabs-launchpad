with source as (

    select * from {{ source('raw_stackexchange', 'raw_questions') }}

),

renamed as (

    select
        -- ids
        question_id,
        owner__user_id                          as user_id,
        accepted_answer_id,

        -- text
        title                                    as question_title,
        link                                     as question_link,
        content_license,

        -- owner info
        owner__display_name                      as owner_display_name,
        owner__reputation                        as owner_reputation,
        owner__user_type                         as owner_user_type,

        -- metrics
        cast(score as integer)                   as score,
        cast(view_count as integer)               as view_count,
        cast(answer_count as integer)              as answer_count,
        cast(is_answered as boolean)               as is_answered,

        -- dates (stored as unix epoch seconds -> cast to timestamp)
        to_timestamp(creation_date)               as created_at,
        to_timestamp(last_activity_date)           as last_activity_at,
        to_timestamp(last_edit_date)               as last_edited_at,
        to_timestamp(closed_date)                  as closed_at,
        closed_reason,

        -- bounty
        cast(bounty_amount as integer)             as bounty_amount,
        to_timestamp(bounty_closes_date)           as bounty_closes_at,

        -- dlt metadata (optional but handy for debugging/lineage)
        _dlt_load_id,
        _dlt_id

    from source
    where question_id is not null and title > 100

)

select * from renamed