# backend/utils/weaviate_client.py

import weaviate
import weaviate.classes as wvc
from weaviate.classes.query import MetadataQuery


class WeaviateClient:
    def __init__(self):
        # Connect to your local Docker Weaviate instance
        self.client = weaviate.connect_to_local(skip_init_checks=True)
        self.collection = self._init_collection()

    def _init_collection(self):
        # Create or fetch the HTMLChunk collection
        if "HTMLChunk" not in self.client.collections.list_all():
            return self.client.collections.create(
                name="HTMLChunk",
                vectorizer_config=wvc.config.Configure.Vectorizer.none(),  # we use custom vectors
                properties=[
                    wvc.config.Property(
                        name="chunk",
                        data_type=wvc.config.DataType.TEXT,
                    ),
                    wvc.config.Property(
                        name="url",
                        data_type=wvc.config.DataType.TEXT,
                    ),
                ],
            )
        return self.client.collections.get("HTMLChunk")

    def insert_chunk_with_vector(self, chunk: str, url: str, vector: list[float]):
        self.collection.data.insert(
            properties={
                "chunk": chunk,
                "url": url,
            },
            vector=vector  # custom embedding
        )

    def search_by_vector(self, query_vector: list[float], limit: int = 10):
        """
        Search Weaviate using a query vector, return top `limit` matching chunks.
        """
        results = self.collection.query.near_vector(
            near_vector=query_vector,
            limit=limit,
            return_metadata=MetadataQuery(distance=True)
        )
        return [
            {
                "chunk": obj.properties["chunk"],
                "url": obj.properties["url"],
                "score": obj.metadata.distance,
            }
            for obj in results.objects
        ]

    def is_connected(self):
        """
        Test connection to Weaviate and list collections.
        """
        try:
            collections = self.client.collections.list_all()
            return True, collections
        except Exception as e:
            return False, str(e)

    def close(self):
        self.client.close()


# Singleton to import elsewhere
weaviate_client = WeaviateClient()
