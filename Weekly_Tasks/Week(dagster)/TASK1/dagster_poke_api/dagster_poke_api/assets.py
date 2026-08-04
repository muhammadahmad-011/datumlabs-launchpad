import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_poke_api.incremental_pokeAPI_pipeline import pipeline, pokeapi_source


@dlt_assets(
    dlt_source=pokeapi_source(),
    dlt_pipeline=pipeline,
    name="pokeapi",
    group_name="pokeapi",
)
def pokeapi_dlt_assets(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

