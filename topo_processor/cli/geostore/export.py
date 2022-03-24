import shutil

import boto3
import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.geostore.invoke import invoke_import_status, invoke_lambda
from topo_processor.util.configuration import temp_folder
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-s",
    "--source",
    required=True,
    help="The source of the data to export",
)
@click.option(
    "-sid",
    "--surveyid",
    required=True,
    help="The survey id of the data to export",
)
@click.option(
    "-st",
    "--surveytitle",
    required=True,
    help="The survey title of the data to export",
)
@click.option(
    "-p",
    "--prod",
    is_flag=True,
    help="Use this flag to export into production environment.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
def main(source: str, surveyid: str, surveytitle: str, prod: str, verbose: str) -> None:
    start_time = time_in_ms()
    if prod:
        target_env = "Production"
    else:
        target_env = "Non Production"
    get_log().info("geostore_export_start", source=source, survey_id=surveyid, surveytitle=surveytitle, environment=target_env)

    if verbose:
        set_level(LogLevel.trace)

    # TODO Where to store that?
    s3_role_arn_nonprod = ""

    client = boto3.client("lambda")
    collection_s3_path = source + "/" + "collection.json"

    if prod:
        environment = "prod"
    else:
        environment = "nonprod"

    try:

        # create a dataset
        create_dataset_parameters = {"title": surveyid, "description": surveytitle}
        dataset_response_payload = invoke_lambda(client, f"{environment}-datasets", "POST", create_dataset_parameters)
        dataset_id = dataset_response_payload["body"]["id"]
        if not dataset_id:
            raise Exception(
                f"No dataset ID found in {environment}-datasets Lambda function response: {dataset_response_payload}"
            )

        # upload data
        upload_data_parameters = {"id": dataset_id, "metadata_url": collection_s3_path, "s3_role_arn": s3_role_arn_nonprod}
        version_response_payload = invoke_lambda(client, f"{environment}-dataset-versions", "POST", upload_data_parameters)
        execution_arn = version_response_payload["body"]["execution_arn"]

        # import status
        import_status = invoke_import_status(client, environment, execution_arn)

        get_log().debug(
            "geostore_export_submitted",
            source=source,
            datasetId=dataset_id,
            execution_arn=execution_arn,
            current_import_status=import_status,
            duration=time_in_ms() - start_time,
            info=f"To check the export status, run the following command 'poetry run status -arn {execution_arn}'",
        )
    except Exception as e:
        get_log().error("geostore_export_failed", err=e)
    finally:
        shutil.rmtree(temp_folder)
