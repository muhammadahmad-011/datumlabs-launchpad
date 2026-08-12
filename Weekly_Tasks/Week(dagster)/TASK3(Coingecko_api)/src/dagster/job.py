import dagster
from dagster import define_asset_job
from .assets import coingecko_dagster_assets


coingecko_job = define_asset_job(
    name="coingecko_ingestion_job",
    selection=[coingecko_dagster_assets],
)