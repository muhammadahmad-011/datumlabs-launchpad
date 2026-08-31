import os
from pathlib import Path

import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_dbt import DagsterDbtTranslator, DbtCliResource, DbtProject, dbt_assets

from pipeline.Coingecko_api import coingecko_source, pipeline


@dlt_assets(
    dlt_source=coingecko_source(),
    dlt_pipeline=pipeline,
    group_name="coingecko",
)
def coingecko_dagster_assets(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


@dg.asset_check(
    asset=dg.AssetKey("dlt_coingecko_source_markets"),
    description="Validates that markets asset is not empty and has valid market identifiers.",
)
def check_markets_data_quality(context: dg.AssetCheckExecutionContext):
    try:
        with pipeline.sql_client() as client:
            row_count = client.execute_sql("SELECT COUNT(*) FROM markets")[0][0]
            null_ids = client.execute_sql("SELECT COUNT(*) FROM markets WHERE id IS NULL")[0][0]
        passed = (row_count > 0) and (null_ids == 0)
        error = None
    except Exception as e:
        context.log.error(f"check_markets_data_quality failed: {e}")
        row_count, null_ids, passed, error = 0, -1, False, str(e)

    return dg.AssetCheckResult(
        passed=passed,
        metadata={
            "total_rows": dg.MetadataValue.int(row_count),
            "null_id_count": dg.MetadataValue.int(null_ids),
            **({"error": dg.MetadataValue.text(error)} if error else {}),
        },
    )


@dg.asset_check(
    asset=dg.AssetKey("dlt_coingecko_source_history"),
    description="Validates price range constraints and record completeness for history asset.",
)
def check_history_data_quality(context: dg.AssetCheckExecutionContext):
    try:
        with pipeline.sql_client() as client:
            invalid_prices = client.execute_sql(
                "SELECT COUNT(*) FROM history WHERE price_usd <= 0"
            )[0][0]
            null_keys = client.execute_sql(
                "SELECT COUNT(*) FROM history WHERE coin_id IS NULL OR date IS NULL"
            )[0][0]
        passed = (invalid_prices == 0) and (null_keys == 0)
        error = None
    except Exception as e:
        context.log.error(f"check_history_data_quality failed: {e}")
        invalid_prices, null_keys, passed, error = -1, -1, False, str(e)

    return dg.AssetCheckResult(
        passed=passed,
        metadata={
            "invalid_price_records": dg.MetadataValue.int(invalid_prices),
            "null_key_records": dg.MetadataValue.int(null_keys),
            **({"error": dg.MetadataValue.text(error)} if error else {}),
        },
    )


# ---------------------------------------------------------------------------
# dbt assets
# ---------------------------------------------------------------------------

DBT_PROJECT_DIR = Path(r"C:\datumlabs-launchpad\Weekly_Tasks\Week(dbt)\dbt_coingecko")

DBT_PROFILES_DIR = Path(os.environ["USERPROFILE"]) / ".dbt"

dbt_project = DbtProject(project_dir=DBT_PROJECT_DIR, profiles_dir=DBT_PROFILES_DIR)

dbt_project.prepare_if_dev()

class CoingeckoDbtTranslator(DagsterDbtTranslator):

    def get_asset_key(self, dbt_resource_props) -> dg.AssetKey:
        if dbt_resource_props["resource_type"] == "source":
            table_name = dbt_resource_props["name"]
            if table_name == "markets":
                return dg.AssetKey("dlt_coingecko_source_markets")
            if table_name == "history":
                return dg.AssetKey("dlt_coingecko_source_history")
        return super().get_asset_key(dbt_resource_props)


@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=CoingeckoDbtTranslator(),
)
def coingecko_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
