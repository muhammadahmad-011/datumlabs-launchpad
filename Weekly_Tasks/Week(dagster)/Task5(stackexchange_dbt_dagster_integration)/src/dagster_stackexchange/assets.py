from dagster import (
    multi_asset, AssetOut, Output,
    AssetExecutionContext, AssetKey,
)
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator

from .constants import DBT_MANIFEST_PATH
from pipeline.stack_exchange_pipeline import run_stackexchange_pipeline

# dlt raw table (source "identifier") -> Dagster asset key
RAW_TABLES = {
    "questions": AssetKey("stackexchange_raw_questions"),
    "answers": AssetKey("stackexchange_raw_answers"),
    "questions__tags": AssetKey("stackexchange_raw_questions_tags"),
}


# dlt asset: one dlt run, one Dagster output per raw table it loads
@multi_asset(
    outs={name: AssetOut(key=key, group_name="dlt") for name, key in RAW_TABLES.items()},
    compute_kind="dlt",
)
def stackexchange_raw_data(context: AssetExecutionContext):
    """Extracts Stack Exchange questions, answers, and tags into DuckDB via dlt."""
    load_info = run_stackexchange_pipeline()
    context.log.info(str(load_info))
    for name in RAW_TABLES:
        yield Output(value=None, output_name=name)


# Maps each dbt source -> its matching dlt asset key, for correct lineage
class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props):
        if dbt_resource_props["resource_type"] == "source":
            identifier = dbt_resource_props.get("identifier") or dbt_resource_props["name"]
            if identifier in RAW_TABLES:
                return RAW_TABLES[identifier]
        return super().get_asset_key(dbt_resource_props)


# dbt assets: runs `dbt build`, using the custom translator above for lineage
@dbt_assets(
    manifest=DBT_MANIFEST_PATH,
    dagster_dbt_translator=CustomDagsterDbtTranslator(),
)
def stackexchange_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()