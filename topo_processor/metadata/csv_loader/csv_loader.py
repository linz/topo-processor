import csv
import os
from curses import meta
from typing import Any, Dict, List

from linz_logger import get_log


def read_csv(metadata_file_path: str, key: str, alternative_key: str = "", columns: List[str] = []) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {}

    csv_path = os.path.join(os.getcwd(), metadata_file_path)
    if not os.path.isfile(csv_path):
        raise Exception(f'Cannot find "{csv_path}"')

    with open(csv_path, "r") as csv_text:
        reader = csv.DictReader(csv_text, delimiter=",")
        for row in reader:
            filtered_row: Dict[str, str] = {}
            if columns:
                for col in columns:
                    filtered_row[col] = row[col]
            else:
                filtered_row = row

            if row[key]:
                key_value = row[key]
                if key_value in metadata:
                    if filtered_row == metadata[key_value]:
                        raise Exception(f'Duplicate "{key_value}" found in "{metadata_file_path}"')
                    elif alternative_key and row[alternative_key]:
                        metadata[row[alternative_key]] = filtered_row
                metadata[key_value] = filtered_row
            elif alternative_key and row[alternative_key]:
                metadata[row[alternative_key]] = filtered_row
            else:
                get_log().debug("read_csv_key_not_found", key=key, alternative_key=alternative_key)
    print("csv_loader " + metadata_file_path)

    return metadata
