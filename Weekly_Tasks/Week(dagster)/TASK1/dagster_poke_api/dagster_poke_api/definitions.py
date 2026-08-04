from dagster import Definitions
from dagster_dlt import DagsterDltResource
from dagster_poke_api.assets import pokeapi_dlt_assets

defs = Definitions(
    assets=[pokeapi_dlt_assets],
    resources={"dlt": DagsterDltResource()},)