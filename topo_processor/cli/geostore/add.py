import json
import shutil
from typing import Any, Dict, List

import boto3
import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.geostore.invoke import invoke_import_status, invoke_lambda
from topo_processor.util.aws_credentials import get_role_arn
from topo_processor.util.aws_files import s3_download
from topo_processor.util.configuration import temp_folder
from topo_processor.util.file_extension import is_tiff
from topo_processor.util.s3 import bucket_name_from_path, is_s3_path
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-s",
    "--source",
    required=True,
    help="The s3 path to the collection.json of the survey to export",
)
@click.option(
    "-c",
    "--commit",
    is_flag=True,
    help="Use this flag to commit the suppression of the dataset",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
def main(source: str, commit: bool, verbose: bool) -> None:
    start_time = time_in_ms()
    get_log().info("geostore_add_started", source=source)

    if verbose:
        set_level(LogLevel.trace)

    try:
        source_role_arn = get_role_arn(bucket_name_from_path(source))
        # Get Collection information
        collection_local_path = f"{temp_folder}/collection.json"

        if is_s3_path(source):
            try:
                s3_download(source, collection_local_path)
            except Exception as e:
                get_log().error("geostore_export_failed", source=source, error=e)
                return
        else:
            print("Exporting local data is not yet implemented")

        with open(collection_local_path) as collection_file:
            collection_json: Dict[str, Any] = json.load(collection_file)
            # Get survey id for dataset id and collection.title for Description
        survey_id = collection_json["summaries"]["mission"][0]
        if not survey_id:
            raise Exception("No survey ID found in collection.json")
        title = collection_json["title"]

        if not commit:
            client_sts = boto3.client("sts")
            client_sts.assume_role(RoleArn=source_role_arn, RoleSessionName="read-session")
            file_list: List[str] = []
            paginator = client_sts.get_paginator("list_objects_v2")
            response_iterator = paginator.paginate(Bucket=source.replace("collection.json", ""))
            for response in response_iterator:
                for contents_data in response["Contents"]:
                    key = contents_data["Key"]
                    if is_tiff(key):
                        file_list.append(key)
            get_log().info(
                "The change won't be commit since the --commit flag has not been specified.",
                sourceFiles=file_list,
                surveyId=survey_id,
                surveyTite=title,
            )
        else:
            # Create a dataset
            create_dataset_parameters = {"title": survey_id, "description": title}
            dataset_response_payload = invoke_lambda("datasets", "POST", create_dataset_parameters)
            dataset_id = dataset_response_payload["body"]["id"]
            if not dataset_id:
                raise Exception(f"No dataset ID found in datasets Lambda function response: {dataset_response_payload}")
            # Upload data
            upload_data_parameters = {"id": dataset_id, "metadata_url": source, "s3_role_arn": source_role_arn}
            version_response_payload = invoke_lambda("dataset-versions", "POST", upload_data_parameters)
            execution_arn = version_response_payload["body"]["execution_arn"]
            # Import status
            import_status = invoke_import_status(execution_arn)

        get_log().debug(
            "geostore_add_completed",
            source=source,
            datasetId=dataset_id,
            executionArn=execution_arn,
            currentImportStatus=import_status,
            duration=time_in_ms() - start_time,
            info=f"To check the export status, run the following command 'poetry run status -arn {execution_arn}'",
        )
    except Exception as e:
        get_log().error("geostore_add_failed", err=e)
    finally:
        shutil.rmtree(temp_folder)
