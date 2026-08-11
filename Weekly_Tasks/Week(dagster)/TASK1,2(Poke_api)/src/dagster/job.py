import dagster as dg
from dagster_poke_api.assets import pokeapi_dlt_assets


pokeapi_job = dg.define_asset_job(
    name="pokeapi_job",
    selection=[pokeapi_dlt_assets],
)
