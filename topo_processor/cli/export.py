import json
import os
from typing import Any, Dict
from urllib.parse import urlparse

import boto3
import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.file_system import manifest
from topo_processor.metadata.data_type import DataType
from topo_processor.util.aws_files import s3_download
from topo_processor.util.configuration import temp_folder
from topo_processor.util.s3 import is_s3_path
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-s",
    "--source",
    required=True,
    help="The source of the data to export",
)
@click.option(
    "-d",
    "--datatype",
    required=True,
    type=click.Choice([data_type for data_type in DataType], case_sensitive=True),
    help="The datatype of the survey to export",
)
@click.option(
    "-cid",
    "--correlationid",
    required=False,
    help="The correlation ID of the batch job",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
@click.option(
    "-p",
    "--prod",
    is_flag=True,
    help="Use this flag to export into production environment.",
)
def main(source: str, datatype: str, correlationid: str, verbose: str, prod: str) -> None:
    get_log().info("export_start", id=correlationid, source=source, dataType=datatype)

    if verbose:
        set_level(LogLevel.trace)

    if prod:
        environment = "prod"
    else:
        environment = "nonprod"

    # Validate source
    collection_path = f"{temp_folder}/collection.json"
    if is_s3_path(source):
        if source.endswith("/"):
            source = source[:-1]
        try:
            s3_download(source + "/" + "collection.json", collection_path)
        except Exception as e:
            get_log().error("export_failed", id=correlationid, source=source, error=e)
    else:
        print("Exporting local data is not yet implemented")

    with open(collection_path) as collection_file:
        collection_json: Dict[str, Any] = json.load(collection_file)

    print(collection_json["summaries"]["mission"])

    # Get survey id for dataset id and collection.title for Description

    """ start_time = time_in_ms()
    data_type = DataType(datatype)
    client = boto3.client("lambda")

    # create a dataset
    dataset_id = client.invoke(
        FunctionName=f"{environment}-datasets",
        InvocationType="RequestResponse",
        LogType="Tail",
        ClientContext="string",
        Payload=b'{"http_method": "POST", "body": {"title":'
        + collection_json["summaries"]["mission"]
        + b', "description": "Description"}}',
        Qualifier="string",
    )

    try:
        print("start")
    finally:
        print("end")
        get_log().debug(
            "Job Completed",
            source=source,
            datasetId=dataset_id,
            dataType=data_type,
            duration=time_in_ms() - start_time,
        ) """
