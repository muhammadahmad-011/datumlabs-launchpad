import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from Pipeline.incremental_pokeAPI_pipeline import pipeline, pokeapi_source
from dagster_dbt import DagsterDbtTranslator, DbtCliResource, dbt_assets
from .project import dbt_poke_api_project

@dlt_assets(
    dlt_source=pokeapi_source(),
    dlt_pipeline=pipeline,
    name="pokeapi",
    group_name="pokeapi",
)
def pokeapi_dlt_assets(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

_dlt_asset_keys_by_table_name = {key.path[-1]: key for key in pokeapi_dlt_assets.keys}

class PokeApiDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props):
        if dbt_resource_props["resource_type"] == "source":
            source_table = dbt_resource_props["name"].lower()
            for key in pokeapi_dlt_assets.keys:
                key_name = key.path[-1].lower()
                if (
                    key_name == source_table
                    or key_name == f"dlt_pokeapi_source_{source_table}"
                    or key_name.endswith(f"_{source_table}")
                ):
                    return key

        return super().get_asset_key(dbt_resource_props)

    def get_group_name(self, dbt_resource_props) -> str:
        return "dbt_poke_api"


@dbt_assets(
    manifest=dbt_poke_api_project.manifest_path,
    project=dbt_poke_api_project,
    dagster_dbt_translator=PokeApiDbtTranslator(),
)
def dbt_poke_api_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()