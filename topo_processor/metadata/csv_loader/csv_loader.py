import csv
import os
from typing import Any, Dict


def read_csv(metadata_file: str = "") -> Dict[str, Any]:
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
            else:
                metadata[row["sufi"]] = row

    return metadata
