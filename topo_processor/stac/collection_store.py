from .collection import Collection

collection_store = {}


def get_collection(title) -> Collection:
    if title not in collection_store:
        create_collection(title)
    return collection_store[title]


def create_collection(title):
    collection = Collection(title)
    collection_store[title] = collection
