import csv
import os
from typing import Any, Dict, List

from linz_logger import get_log


def read_csv(metadata_file: str) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {}

    csv_path = os.path.join(os.getcwd(), metadata_file)
    if not os.path.isfile(csv_path):
        raise Exception(f'Cannot find "{csv_path}"')

    with open(csv_path, "r") as csv_text:
        reader = csv.DictReader(csv_text, delimiter=",")
        for row in reader:
            if row["raw_filename"]:
                raw_filename = row["raw_filename"]
                if raw_filename in metadata:
                    if row == metadata[raw_filename]:
                        raise Exception(f'Duplicate file "{raw_filename}" found in metadata csv')
                    else:
                        metadata[row["sufi"]] = row
                metadata[raw_filename] = row
            elif row["sufi"]:
                metadata[row["sufi"]] = row

    return metadata


def load_data(metadata_file_path: str, key: str, alternative_key: str = "", columns: List[str] = []) -> Dict[str, Any]:
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
                        raise Exception(f'Duplicate "{key_value}" found in metadata csv')
                    elif alternative_key and row[alternative_key]:
                        metadata[row[alternative_key]] = filtered_row
                metadata[key_value] = filtered_row
            elif alternative_key and row[alternative_key]:
                metadata[row[alternative_key]] = filtered_row
            else:
                get_log().debug("load_data_key_not_found", key=key, alternative_key=alternative_key)

    return metadata
