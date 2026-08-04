import dagster as dg
from dagster_poke_api.assets import pokeapi_dlt_assets

pokeapi_job = dg.define_asset_job(
    name="pokeapi_job",
    selection=[pokeapi_dlt_assets],
)

pokeapi_schedule = dg.ScheduleDefinition(
    name="pokeapi_daily_schedule",
    job=pokeapi_job,
    cron_schedule="10 18 * * *",
    execution_timezone="Asia/Karachi",
)