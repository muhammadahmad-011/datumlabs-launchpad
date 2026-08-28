with question_tags as (

    select * from {{ ref('int_questions_tags') }}

),

questions as (

    select * from {{ ref('stg_stack_exchange__questions') }}

),

joined as (

    select
        question_tags.tag_name,
        questions.question_id,
        questions.view_count,
        questions.answer_count,
        questions._dlt_load_id

    from question_tags
    left join questions
        on question_tags.question_id = questions.question_id

)

select * from joined