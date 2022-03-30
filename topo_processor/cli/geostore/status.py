import boto3
import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.geostore.invoke import invoke_import_status
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-arn",
    "--executionarn",
    required=True,
    help="The execution arn received from the Geostore after invoking an upload",
)
@click.option(
    "-p",
    "--prod",
    is_flag=True,
    help="Use this flag to get the status from the production environment",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
def main(executionarn: str, prod: bool, verbose: bool) -> None:
    start_time = time_in_ms()
    get_log().info("check_export_status_start", arn=executionarn, isProduction=prod)

    if verbose:
        set_level(LogLevel.trace)

    client = boto3.client("lambda")

    try:
        # import status
        import_status = invoke_import_status(client, executionarn, prod)

        get_log().debug(
            "check_export_status_end",
            current_export_status=import_status,
            isProduction=prod,
            duration=time_in_ms() - start_time,
        )
    except Exception as e:
        get_log().error("check_export_status_failed", err=e)
