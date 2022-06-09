import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.geostore.invoke import invoke_lambda
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-d",
    "--dataset-id",
    required=True,
    help="The dataset id to delete",
)
@click.option(
    "-c",
    "--commit",
    is_flag=True,
    help="Use this flag to commit the suppression of the dataset.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display debug logs",
)
def main(dataset_id: str, commit: bool, verbose: str) -> None:
    start_time = time_in_ms()
    logger = get_log()
    logger.info("delete_datasets_start", dataset_id=dataset_id)

    if not verbose:
        set_level(LogLevel.info)

    try:
        delete_parameters = {"title": dataset_id}
        operation = "GET"
        if commit:
            operation = "DELETE"

        response = invoke_lambda("datasets", operation, delete_parameters)
        if not commit:
            logger.info(
                f"You are about to delete the following dataset: {response['body']}. Run the command again with the --commit flag to confirm."
            )
        else:
            logger.info("delete_dataset_success", deleted_id=dataset_id, duration=time_in_ms() - start_time)
    except Exception as e:
        logger.error("delete_dataset_failed", err=e)
