with source as (

    select * from {{ source('raw_stackexchange', 'raw_answers') }}

),

renamed as (

    select
        -- ids
        answer_id,
        question_id,
        owner__user_id                          as user_id,

        -- content
        content_license,

        -- owner info
        owner__display_name                      as owner_display_name,
        owner__reputation                        as owner_reputation,
        owner__user_type                         as owner_user_type,

        -- metrics
        cast(score as integer)                   as score,
        cast(is_accepted as boolean)              as is_accepted,

        -- dates (unix epoch seconds -> timestamp)
        to_timestamp(creation_date)               as created_at,
        to_timestamp(last_activity_date)           as last_activity_at,
        to_timestamp(last_edit_date)               as last_edited_at,

        -- dlt metadata
        _dlt_load_id,
        _dlt_id

    from source
    where answer_id is not null

)

select * from renamed