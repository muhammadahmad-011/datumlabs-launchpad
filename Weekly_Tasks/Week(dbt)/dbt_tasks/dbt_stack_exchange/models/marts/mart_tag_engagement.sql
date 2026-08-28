{{ config(
    materialized='incremental',
    unique_key='tag_name',
    incremental_strategy='delete+insert'
) }}

with tag_question_metrics as (

    select * from {{ ref('int_tag_question_metrics') }}

    {% if is_incremental() %}
    where tag_name in (
        select distinct tag_question_metrics.tag_name
        from {{ ref('int_tag_question_metrics') }} as tag_question_metrics
        where tag_question_metrics._dlt_load_id > (select coalesce(max(max_dlt_load_id), '0') from {{ this }})
    )
    {% endif %}

),

answers as (

    select * from {{ ref('stg_stack_exchange__answers') }}

),

tag_answer_counts as (

    select
        tag_question_metrics.tag_name,
        count(answers.answer_id) as answer_count_actual

    from tag_question_metrics
    left join answers
        on tag_question_metrics.question_id = answers.question_id

    group by tag_question_metrics.tag_name

),

aggregated as (

    select
        tag_question_metrics.tag_name,
        count(distinct tag_question_metrics.question_id) as total_questions,
        sum(tag_question_metrics.view_count)               as total_views,
        sum(tag_question_metrics.answer_count)              as total_answer_count_from_questions,
        max(tag_question_metrics._dlt_load_id)              as max_dlt_load_id

    from tag_question_metrics
    group by tag_question_metrics.tag_name

)

select
    aggregated.tag_name,
    aggregated.total_questions,
    aggregated.total_views,
    tag_answer_counts.answer_count_actual as total_answers,
    aggregated.total_answer_count_from_questions,
    aggregated.max_dlt_load_id

from aggregated
left join tag_answer_counts
    on aggregated.tag_name = tag_answer_counts.tag_name

order by aggregated.total_views desc