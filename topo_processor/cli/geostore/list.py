import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.geostore.invoke import invoke_lambda
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-d",
    "--dataset-id",
    required=False,
    help="The dataset id to filter",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
def main(dataset_id: str, verbose: bool) -> None:
    start_time = time_in_ms()
    get_log().info("list_datasets_start", dataset_id=dataset_id)

    if verbose:
        set_level(LogLevel.trace)

    try:
        list_parameters = {}
        if dataset_id:
            list_parameters = {"id": dataset_id}
        dataset_list = invoke_lambda("datasets", "GET", list_parameters)

        get_log().debug("list_datasets_end", dataset_list=dataset_list, duration=time_in_ms() - start_time)
    except Exception as e:
        get_log().error("list_datasets_failed", err=e)
