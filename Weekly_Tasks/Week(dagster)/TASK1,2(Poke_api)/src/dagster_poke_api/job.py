import dagster as dg
from .assets import pokeapi_dlt_assets, dbt_poke_api_dbt_assets


pokeapi_job = dg.define_asset_job(
    name="pokeapi_job",
    selection=[pokeapi_dlt_assets,dbt_poke_api_dbt_assets],
)