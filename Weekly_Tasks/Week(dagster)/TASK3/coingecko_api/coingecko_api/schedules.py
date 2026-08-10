import dagster
from dagster import ScheduleDefinition
from coingecko_api.job import coingecko_job

coingecko_daily_schedule = ScheduleDefinition(
    name="coingecko_daily_schedule",
    job=coingecko_job,
    cron_schedule="0 8 * * *",
    execution_timezone="Asia/Karachi",
)