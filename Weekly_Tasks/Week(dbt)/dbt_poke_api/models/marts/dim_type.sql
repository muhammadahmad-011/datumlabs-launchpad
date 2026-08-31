select
    type_id,
    type_name,
    generation
from {{ ref('stg_type') }}
