import shutil

import boto3
import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.geostore.environment import is_production
from topo_processor.geostore.invoke import invoke_import_status, invoke_lambda
from topo_processor.util.configuration import temp_folder
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-s",
    "--source",
    required=True,
    help="The s3 path to the collection.json of the survey to export",
)
@click.option(
    "-i",
    "--survey-id",
    required=True,
    help="The survey id of the data to export",
)
@click.option(
    "-t",
    "--survey-title",
    required=True,
    help="The survey title of the data to export",
)
@click.option(
    "-r",
    "--role-arn",
    required=True,
    help="The survey title of the data to export",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
def main(source: str, survey_id: str, survey_title: str, role_arn: str, verbose: bool) -> None:
    start_time = time_in_ms()
    get_log().info("geostore_export_start", source=source, surveyId=survey_id, surveyTitle=survey_title)

    if verbose:
        set_level(LogLevel.trace)

    client = boto3.client("lambda")

    try:
        # create a dataset
        create_dataset_parameters = {"title": survey_id, "description": survey_title}
        dataset_response_payload = invoke_lambda(client, "datasets", "POST", create_dataset_parameters)
        dataset_id = dataset_response_payload["body"]["id"]
        if not dataset_id:
            raise Exception(f"No dataset ID found in datasets Lambda function response: {dataset_response_payload}")

        # upload data
        upload_data_parameters = {"id": dataset_id, "metadata_url": source, "s3_role_arn": role_arn}
        version_response_payload = invoke_lambda(client, "dataset-versions", "POST", upload_data_parameters)
        execution_arn = version_response_payload["body"]["execution_arn"]

        # import status
        import_status = invoke_import_status(client, execution_arn)

        get_log().debug(
            "geostore_export_submitted",
            source=source,
            datasetId=dataset_id,
            executionArn=execution_arn,
            currentImportStatus=import_status,
            duration=time_in_ms() - start_time,
            isProduction=is_production,
            info=f"To check the export status, run the following command 'poetry run status -arn {execution_arn}'",
        )
    except Exception as e:
        get_log().error("geostore_export_failed", err=e)
    finally:
        shutil.rmtree(temp_folder)
