import boto3
import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.geostore.invoke import invoke_import_status
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-a",
    "--execution-arn",
    required=True,
    help="The execution arn received from the Geostore after invoking an upload",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
def main(execution_arn: str, verbose: bool) -> None:
    start_time = time_in_ms()
    get_log().info("check_export_status_start", arn=execution_arn)

    if verbose:
        set_level(LogLevel.trace)

    try:
        # import status
        import_status = invoke_import_status(execution_arn)

        get_log().debug(
            "check_export_status_end",
            current_export_status=import_status,
            duration=time_in_ms() - start_time,
        )
    except Exception as e:
        get_log().error("check_export_status_failed", err=e)
