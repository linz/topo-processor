import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.geostore.invoke import invoke_lambda
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-s",
    "--title",
    required=False,
    help="The Geostore title of the survey to filter",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display debug logs",
)
def main(title: str, verbose: bool) -> None:
    start_time = time_in_ms()
    logger = get_log()
    logger.info("list_datasets_start", title=title)

    if not verbose:
        set_level(LogLevel.info)

    try:
        list_parameters = {}
        if title:
            list_parameters = {"title": title}
        dataset_list = invoke_lambda("datasets", "GET", list_parameters)

        logger.info("list_datasets_end", dataset_list=dataset_list, duration=time_in_ms() - start_time)
    except Exception as e:
        logger.error("list_datasets_failed", err=e)
