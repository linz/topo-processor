import boto3
import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.geostore.invoke import invoke_lambda
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-id",
    "--dataset-id",
    required=True,
    help="The dataset id to delete.",
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
def main(dataset_id: str, prod: bool, verbose: str) -> None:
    start_time = time_in_ms()
    get_log().info("delete_datasets_start", dataset_id=dataset_id, isProduction=prod)

    if verbose:
        set_level(LogLevel.trace)

    client = boto3.client("lambda")

    try:
        delete_parameters = {"id": dataset_id}
        response = invoke_lambda(client, "datasets", "DELETE", delete_parameters, prod)
        if response["status_code"] != 204:
            raise Exception("An issue occured during the deletion", response)

        get_log().debug("delete_dataset_success", deleted_id=dataset_id, isProduction=prod, duration=time_in_ms() - start_time)
    except Exception as e:
        get_log().error("delete_dataset_failed", err=e)
