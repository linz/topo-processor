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


def read_gpkg(metadata_file_path: str, key: str, alternative_key: str = "", columns: List[str] = []) -> Dict[str, Any]:

    #metadata_path = os.path.join(os.getcwd(), "test_data", "51002_338399.gpkg")
    metadata: Dict[str, Any] = {}

    gpkg_path = os.path.join(os.getcwd(), metadata_file_path)
    if not os.path.isfile(gpkg_path):
        raise Exception(f'Cannot find "{gpkg_path}"')

    gpkg_connection = sqlite3.connect(gpkg_path)
    gpkg_cursor = gpkg_connection.cursor()

    #get table name in a flexible way

    #filtered_row: Dict[str, str] = {}

    if columns:
        #do stuff for survey footprint file
        print("survey footprint")
    else:
        print("photo footprint")
        gpkg_cursor.execute(f"SELECT * from 'nz_aerial_photo_footprints_mainland_nz_1936_2005_polygons' WHERE RAW_FILENAME = {key};")
        filtered_row = gpkg_cursor.fetchall()
        if len(filtered_row) > 1:
            raise Exception(f'Duplicate "{key}" found in "{metadata_file_path}"')

        column_names = [description[0] for description in gpkg_cursor.description]
        metadata = dict(zip(column_names, filtered_row[0]))


    #gpkg_cursor.execute("SELECT * from 'historic_aerial_photos_survey_footprints_crown_1936_2005' LIMIT 100;")






    return metadata
