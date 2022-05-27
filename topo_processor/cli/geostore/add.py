import json
import os
import shutil
from typing import Any, Dict, List
from urllib.parse import urlparse

import boto3
import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.geostore.invoke import invoke_import_status, invoke_lambda
from topo_processor.util.aws_credentials import Credentials
from topo_processor.util.aws_files import s3_download
from topo_processor.util.configuration import temp_folder
from topo_processor.util.file_extension import is_tiff
from topo_processor.util.s3 import is_s3_path
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-s",
    "--source",
    required=True,
    help="The s3 path to the survey to export",
)
@click.option(
    "-r",
    "--role",
    required=True,
    help="The ARN role to access to the source bucket",
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
def main(source: str, role: str, commit: bool, verbose: bool) -> None:
    start_time = time_in_ms()
    get_log().info("geostore_add_started", source=source)

    if verbose:
        set_level(LogLevel.trace)

    try:
        source_role_arn = role
        client_sts = boto3.client("sts")
        assumed_role = client_sts.assume_role(RoleArn=source_role_arn, RoleSessionName="read-session")
        # Get Collection information
        collection_local_path = os.path.join(temp_folder, "collection.json")

        if is_s3_path(source):
            try:
                credentials = Credentials(
                    assumed_role["Credentials"]["AccessKeyId"],
                    assumed_role["Credentials"]["SecretAccessKey"],
                    assumed_role["Credentials"]["SessionToken"],
                )
                s3_download(os.path.join(source, "collection.json"), collection_local_path, credentials)
            except Exception as e:
                get_log().error("geostore_export_failed", source=source, error=e)
                return
        else:
            raise Exception("The source has to be a survey in a S3 bucket.")

        with open(collection_local_path) as collection_file:
            collection_json: Dict[str, Any] = json.load(collection_file)
            # Get survey id for dataset id and collection.title for Description
        survey_id = collection_json["summaries"]["mission"][0]
        if not survey_id:
            raise Exception("No survey ID found in collection.json")
        title = collection_json["title"]

        if not commit:
            source_parse = urlparse(source, allow_fragments=False)
            bucket_name = source_parse.netloc
            prefix = source_parse.path[1:].replace("collection.json", "")
            get_log().debug("no_commit", action="list_objects", bucket=bucket_name, prefix=prefix)
            file_list: List[str] = []
            s3 = boto3.client(
                "s3",
                aws_access_key_id=credentials.access_key,
                aws_secret_access_key=credentials.secret_key,
                aws_session_token=credentials.token,
            )
            paginator = s3.get_paginator("list_objects_v2")
            response_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
            for response in response_iterator:
                get_log().debug("list_objects_response", response=response)
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
            # Check if a dataset for this survey already exists
            list_parameters = {"title": survey_id}
            dataset_list = invoke_lambda("datasets", "GET", list_parameters)
            if len(dataset_list["body"]) == 1 and dataset_list["body"][0]["title"] == survey_id:
                if click.confirm(
                    f"A dataset for the survey {survey_id} already exist. A new version will be created. Do you want to continue?",
                    abort=True,
                ):
                    dataset_id = dataset_list["body"][0]["id"]
                    click.echo("A new version will be created.")
            else:
                get_log().info("create_dataset")
                # Create a dataset
                create_dataset_parameters = {"title": survey_id, "description": title}
                dataset_response_payload = invoke_lambda("datasets", "POST", create_dataset_parameters)
                dataset_id = dataset_response_payload["body"]["id"]
                if not dataset_id:
                    raise Exception(f"No dataset ID found in datasets Lambda function response: {dataset_response_payload}")

            # Upload data
            upload_data_parameters = {
                "id": dataset_id,
                "metadata_url": os.path.join(source, "collection.json"),
                "s3_role_arn": source_role_arn,
            }
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
                info=f"To check the export status, run the following command 'poetry run status -a {execution_arn}'",
            )
    except Exception as e:
        get_log().error("geostore_add_failed", err=e)
    finally:
        shutil.rmtree(temp_folder)
