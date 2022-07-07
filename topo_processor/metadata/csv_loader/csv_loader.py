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


def read_gpkg(metadata_file_path: str, criteria: Dict[str, str], key:str, columns: List[str] = []) -> Dict[str, Any]:

    metadata: Dict[str, Any] = {}
    selected_row: Dict[str, str] = {}
    new_row: Dict[str, str] = {}

    gpkg_path = os.path.join(os.getcwd(), metadata_file_path)
    if not os.path.isfile(gpkg_path):
        raise Exception(f'Cannot find "{gpkg_path}"')

    gpkg_connection = sqlite3.connect(gpkg_path)
    gpkg_cursor = gpkg_connection.cursor()
    gpkg_cursor.execute("SELECT table_name FROM 'gpkg_contents'")
    table_name = gpkg_cursor.fetchone()[0]
    print(table_name)
    sql_command = "SELECT * FROM " + table_name + " WHERE " + key + " = :" + key + ";"
    gpkg_cursor.execute(sql_command, criteria)

    selected_row = gpkg_cursor.fetchall()

    column_names = [description[0] for description in gpkg_cursor.description]
    if len(selected_row) > 1:
        raise Exception(f'Duplicate "{criteria}" found in "{metadata_file_path}"')
    if len(selected_row) == 0:
        return metadata

    metadata_col_names = dict(zip(column_names, [str(x) for x in selected_row[0]]))

    if columns:
        for col in columns:
            new_row[col] = metadata_col_names[col]
            metadata[criteria[key]] = new_row

    else:
        metadata[criteria[key]] = metadata_col_names

    gpkg_connection.close

    return metadata
