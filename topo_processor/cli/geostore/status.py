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
    help="Use verbose to display debug logs",
)
def main(execution_arn: str, verbose: bool) -> None:
    start_time = time_in_ms()
    logger = get_log()
    logger.info("check_import_status_start", arn=execution_arn)

    if not verbose:
        set_level(LogLevel.info)

    try:
        import_status = invoke_import_status(execution_arn)

        logger.info(
            "check_import_status",
            current_import_status=import_status,
        )

        logger.debug(
            "check_export_status_end",
            duration=time_in_ms() - start_time,
        )

    except Exception as e:
        logger.error("check_import_status_failed", err=e)
