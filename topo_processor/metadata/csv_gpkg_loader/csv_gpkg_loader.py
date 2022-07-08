import csv
import os
import sqlite3
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

    return metadata


def read_gpkg(metadata_file_path: str, criteria: Dict[str, str], key: str, columns: List[str] = []) -> Dict[str, Any]:

    metadata: Dict[str, Any] = {}
    new_row: Dict[str, str] = {}
    metadata_col_names: Dict[str, Any] = {}

    query_key = list(criteria.keys())[0]

    gpkg_path = os.path.join(os.getcwd(), metadata_file_path)
    if not os.path.isfile(gpkg_path):
        raise Exception(f'Cannot find "{gpkg_path}"')
    gpkg_connection = sqlite3.connect(gpkg_path)
    gpkg_cursor = gpkg_connection.cursor()

    gpkg_cursor.execute("SELECT table_name FROM 'gpkg_contents'")
    table_name = gpkg_cursor.fetchone()[0]

    sql_command = "SELECT * FROM " + table_name + " WHERE " + query_key + " = :" + query_key + ";"
    gpkg_cursor.execute(sql_command, criteria)

    selected_rows = gpkg_cursor.fetchall()

    column_names = [description[0] for description in gpkg_cursor.description]

    if len(selected_rows) > 1 and query_key == "raw_filename":
        raise Exception(f'Duplicate "{criteria}" found in "{metadata_file_path}"')
    if len(selected_rows) == 0:
        return metadata

    for row in selected_rows:
        temp_dict = dict(zip(column_names, [str(x) for x in row]))
        metadata[temp_dict[key]] = temp_dict

    print(metadata_col_names)

    if columns:
        for col in columns:
            new_row[col] = metadata_col_names[col]
            metadata[criteria[key]] = new_row

    # else:
    #     metadata[criteria[key]] = metadata_col_names

    gpkg_connection.close

    return metadata
