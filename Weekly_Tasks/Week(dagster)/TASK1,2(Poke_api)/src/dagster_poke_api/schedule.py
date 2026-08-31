import dagster as dg
from .assets import pokeapi_dlt_assets
from .job import pokeapi_job

pokeapi_schedule = dg.ScheduleDefinition(
    name="pokeapi_daily_schedule",
    job=pokeapi_job,
    cron_schedule="10 18 * * *",
    execution_timezone="Asia/Karachi",
)