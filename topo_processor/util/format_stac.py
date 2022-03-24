from heapq import merge
from typing import Any, Dict

def order_stac_collection(collection_dict: Dict[str, Any], data_type: str) -> Dict[str, Any]:

    if data_type == "imagery.historic":

        new_dict: Dict[str, Any] = {}

        new_dict["type"] = collection_dict.pop("type")
        new_dict["stac_version"] = collection_dict.pop("stac_version")
        new_dict["stac_extensions"] = collection_dict.pop("stac_extensions")
        new_dict["id"] = collection_dict.pop("id")
        new_dict["title"] = collection_dict.pop("title")
        new_dict["description"] = collection_dict.pop("description")
        new_dict["license"] = collection_dict.pop("license")
        new_dict["providers"] = collection_dict.pop("providers")
        new_dict["extent"] = collection_dict.pop("extent")

        new_dict.update(collection_dict)

        return new_dict

    else:
        return collection_dict
