import dlt
from github import github_reactions

def run_github_pipeline():
    # Define the pipeline engine
    pipeline = dlt.pipeline(
        pipeline_name="github_reactions_pipeline",
        destination="duckdb",
        dataset_name="github_data"
    )

    # Configure the source/resource with parameters
    data = github_reactions(
        owner="dlt-hub",
        name="dlt",
        items_per_page=100,
        max_items=200)

    # Execute the extraction and load process
    load_info = pipeline.run(data)
    print(load_info)

    #  Print the generated schema definition
    print(pipeline.default_schema.to_pretty_yaml())


run_github_pipeline()