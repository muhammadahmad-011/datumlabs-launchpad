with questions as (

    select * from {{ ref('stg_stack_exchange__questions') }}

),

answers as (

    select * from {{ ref('stg_stack_exchange__answers') }}

),

joined as (

    select
        questions.question_id,
        questions.question_title,
        questions.question_link,
        questions.user_id                as question_owner_id,
        questions.score                  as question_score,
        questions.view_count,
        questions.answer_count,
        questions.is_answered,
        questions.created_at             as question_created_at,

        answers.answer_id,
        answers.user_id                  as answer_owner_id,
        answers.score                    as answer_score,
        answers.is_accepted,
        answers.created_at               as answer_created_at

    from questions
    left join answers
        on questions.question_id = answers.question_id

)

select * from joined