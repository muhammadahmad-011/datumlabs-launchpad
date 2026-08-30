from dagster import Definitions
from dagster_dbt import DbtCliResource

from .assets import stackexchange_raw_data, stackexchange_dbt_assets
from .constants import DBT_PROJECT_DIR
from .job import stackexchange_job

defs = Definitions(
    assets=[stackexchange_raw_data, stackexchange_dbt_assets],
    resources={
        "dbt": DbtCliResource(project_dir=DBT_PROJECT_DIR),
    },
    jobs=[stackexchange_job],
)