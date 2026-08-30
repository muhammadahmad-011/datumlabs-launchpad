from dagster import define_asset_job, AssetSelection

stackexchange_job = define_asset_job(
    name="stackexchange_full_refresh",
    selection=AssetSelection.all(),
)