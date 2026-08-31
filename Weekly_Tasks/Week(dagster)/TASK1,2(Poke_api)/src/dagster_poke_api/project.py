from pathlib import Path
from dagster_dbt import DbtProject

DBT_PROJECT_DIR = (
    Path(__file__).resolve().parents[4]
    / "Week(dbt)"
    / "dbt_poke_api"
)

dbt_poke_api_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=Path.home() / ".dbt",
)

dbt_poke_api_project.prepare_if_dev()