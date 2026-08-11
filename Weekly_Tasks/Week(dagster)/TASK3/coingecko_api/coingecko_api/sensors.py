import os
from dagster import (RunFailureSensorContext, run_failure_sensor, DefaultSensorStatus,
                    run_status_sensor, DagsterRunStatus, RunStatusSensorContext)
from dagster_slack import SlackResource
from dotenv import load_dotenv
import datetime

load_dotenv()

slack_datum = SlackResource(token=os.getenv("SLACK_BOT_TOKEN_DATUM"))
base_url = "http://localhost:3000"

@run_failure_sensor(
    description="Sends alerts to Slack when a Dagster job run fails",
    default_status= DefaultSensorStatus.RUNNING
)
def slack_on_run_failure(context: RunFailureSensorContext) -> None:

    try:        
        complete_url = f"{base_url}/runs/{context.dagster_run.run_id}"

        alert_time = datetime.datetime.now().strftime("%b %d, %Y %H:%M:%S")
    
        message = (
            f"*Dagster Alert Notification* :rotating_light: \n"
            f"*Job Name* - {context.dagster_run.job_name}\n"
            f"*Job Run ID* - {context.dagster_run.run_id}\n"
            f"*Job Status* - FAILED\n"
            f"*Alert Time* - {alert_time}\n"
            f"*Check Error Logs here* - {complete_url}"
        )

        slack_datum.get_client().chat_postMessage(channel="launchpad-technical", text=message)
       
    except Exception as e:
        message = (
            f"Failed to send Slack notification for \n"
            f"*Job Name* - {context.dagster_run.job_name}\n"
            f"*Job Run ID* - {context.dagster_run.run_id}\n"
            f"*Error status* - {e}" 
        )
        slack_datum.get_client().chat_postMessage(channel="launchpad-technical", text=message)


@run_status_sensor(
    run_status = DagsterRunStatus.CANCELED,
    description = "Alerts when a run is canceled / terminated",
    default_status = DefaultSensorStatus.RUNNING
)
def slack_on_run_canceled(context: RunStatusSensorContext) -> None:
    try:        
        complete_url = f"{base_url}/runs/{context.dagster_run.run_id}"

        alert_time = datetime.datetime.now().strftime("%b %d, %Y %H:%M:%S")
    
        message = (
            f"*Dagster Alert Notification* :rotating_light: \n"
            f"*Job Name* - {context.dagster_run.job_name}\n"
            f"*Job Run ID* - {context.dagster_run.run_id}\n"
            f"*Job Status* - CANCELED / Terminated \n"
            f"*Alert Time* - {alert_time}\n"
            f"*Check Error Logs here* - {complete_url}"
        )

        slack_datum.get_client().chat_postMessage(channel="launchpad-technical", text=message)
       
    except Exception as e:
        message = (
            f"Failed to send Slack notification for \n"
            f"*Job Name* - {context.dagster_run.job_name}\n"
            f"*Job Run ID* - {context.dagster_run.run_id}\n"
            f"*Error status* - {e}" 
        )
        slack_datum.get_client().chat_postMessage(channel="launchpad-technical", text=message)