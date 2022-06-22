import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.geostore.invoke import invoke_lambda
from topo_processor.metadata.data_type import DataType
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-s",
    "--survey",
    required=False,
    help="The survey to filter",
)
@click.option(
    "-d",
    "--datatype",
    required=True,
    type=click.Choice([data_type for data_type in DataType], case_sensitive=True),
    help="The datatype of the upload",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display debug logs",
)
def main(survey: str, datatype: str, verbose: bool) -> None:
    start_time = time_in_ms()
    data_type = DataType(datatype)
    logger = get_log()
    logger.info("list_datasets_start", survey=survey)

    if not verbose:
        set_level(LogLevel.info)

    if data_type == DataType.IMAGERY_HISTORIC:
        title_prefix = "historical-aerial-imagery-survey-"
    else:
        raise Exception("Data type not yet implemented")

    try:
        list_parameters = {}
        if survey:
            list_parameters = {"title": title_prefix + survey}
        dataset_list = invoke_lambda("datasets", "GET", list_parameters)

        logger.info("list_datasets_end", dataset_list=dataset_list, duration=time_in_ms() - start_time)
    except Exception as e:
        logger.error("list_datasets_failed", err=e)
