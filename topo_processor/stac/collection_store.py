from .collection import Collection


class CollectionStore:
    collections = {}

    def get_collection(self, title) -> Collection:
        if title not in self.collections:
            self.create_collection(title)
        return self.collections[title]

    def create_collection(self, title):
        collection = Collection(title)
        self.collections[title] = collection
