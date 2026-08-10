--wrong url-- caused error


dagster._core.errors.DagsterExecutionStepExecutionError: Error occurred while executing op "ingest_coingecko":

  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_core\execution\plan\execute_plan.py", line 243, in dagster_event_sequence_for_step
    yield from check.generator(step_events)
  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_core\execution\plan\execute_step.py", line 505, in core_dagster_event_sequence_for_step
    for user_event in _step_output_error_checked_user_event_sequence(
                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        step_context,
        ^^^^^^^^^^^^^
        _process_asset_results_to_events(step_context, user_event_sequence),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ):
    ^
  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_core\execution\plan\execute_step.py", line 184, in _step_output_error_checked_user_event_sequence
    for user_event in user_event_sequence:
                      ^^^^^^^^^^^^^^^^^^^
  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_core\execution\plan\execute_step.py", line 88, in _process_asset_results_to_events
    for user_event in user_event_sequence:
                      ^^^^^^^^^^^^^^^^^^^
  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_core\execution\plan\compute.py", line 188, in execute_core_compute
    for step_output in _yield_compute_results(step_context, inputs, compute_fn, compute_context):
                       ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_core\execution\plan\compute.py", line 157, in _yield_compute_results
    for event in iterate_with_context(
                 ~~~~~~~~~~~~~~~~~~~~^
        lambda: op_execution_error_boundary(
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<7 lines>...
        user_event_generator,
        ^^^^^^^^^^^^^^^^^^^^^
    ):
    ^
  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_utils\__init__.py", line 392, in iterate_with_context
    with context_fn():
         ~~~~~~~~~~^^
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\Lib\contextlib.py", line 162, in __exit__
    self.gen.throw(value)
    ~~~~~~~~~~~~~~^^^^^^^
  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_core\execution\plan\utils.py", line 87, in op_execution_error_boundary
    raise error_cls(
    ...<4 lines>...
    ) from e

The above exception was caused by the following exception:
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://api.coingecko.com/api/v3/coins/market?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false

  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_core\execution\plan\utils.py", line 57, in op_execution_error_boundary
    yield
  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_utils\__init__.py", line 394, in iterate_with_context
    next_output = next(iterator)
  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_core\execution\plan\compute_generator.py", line 136, in _coerce_op_compute_fn_to_iterator
    result = invoke_compute_fn(
        fn, context, kwargs, context_arg_provided, config_arg_class, resource_arg_mapping
    )
  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\dagster\_core\execution\plan\compute_generator.py", line 116, in invoke_compute_fn
    return fn(context, **args_to_pass) if context_arg_provided else fn(**args_to_pass)
                                                                    ~~^^^^^^^^^^^^^^^^
  File "C:\datumlabs-launchpad\Weekly_Tasks\Week(dagster)\TASK3\Task3(pipeline_natively_in_dagster)\dagster_asset\dagster_asset\assets.py", line 27, in ingest_coingecko
    response.raise_for_status()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\datumlabs-launchpad\.venv\Lib\site-packages\requests\models.py", line 1167, in raise_for_status
    raise HTTPError(http_error_msg, response=self)

