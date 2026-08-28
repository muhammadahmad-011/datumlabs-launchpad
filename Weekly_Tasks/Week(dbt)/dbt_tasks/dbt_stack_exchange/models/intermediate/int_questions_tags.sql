with questions as (

    select * from {{ source('raw_stackexchange', 'raw_questions') }}

),

tags as (

    select * from {{ source('raw_stackexchange', 'raw_questions_tags') }}

),

bridged as (

    select
        questions.question_id,
        tags.value as tag_name

    from questions
    left join tags
        on tags._dlt_parent_id = questions._dlt_id

)

select * from bridged