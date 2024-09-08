import weaviate
from weaviate.embedded import EmbeddedOptions
from weaviate.classes.config import Configure, Property, DataType, VectorDistances
from weaviate.classes.query import Filter, MetadataQuery

import torch

try:
    from tqdm import tqdm
except Exception:

    def tqdm(*args, **kwargs):
        return args[0]


def identity_func(x):
    return x


class WeaviateSearchDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        collection,
        query_batch,
        search_kwargs={},
        query_fn=None,
    ):
        self.collection = collection
        self.query_batch = query_batch
        self.search_kwargs = search_kwargs
        self.query_fn = query_fn

    def __len__(self):
        return len(self.query_batch)

    def __getitem__(self, idx):
        query = self.query_batch[idx]
        response = self.collection.query.near_vector(
            near_vector=query, **self.search_kwargs
        )
        if self.query_fn is not None:
            response = self.query_fn(response)
        return response


def batch_search(
    collection,
    query_batch,
    search_kwargs={},
    query_fn=None,
    loader_kwargs={},
    tqdm_kwargs={},
):
    dataset = WeaviateSearchDataset(
        collection,
        query_batch,
        search_kwargs=search_kwargs,
        query_fn=query_fn,
    )
    loader_kwargs.setdefault("collate_fn", identity_func)
    data_loader = torch.utils.data.DataLoader(dataset, **loader_kwargs)
    if tqdm_kwargs is not None:
        data_loader = tqdm(data_loader, **tqdm_kwargs)

    out = []
    for mini_batch in data_loader:
        out.extend(mini_batch)
    return out


def response_to_dict(response, selecting_properties=None):
    out = []
    for o in response.objects:
        if selecting_properties is not None:
            response_dict = {
                k: v for (k, v) in o.properties.items() if k in selecting_properties
            }
        else:
            response_dict = {k: v for (k, v) in o.properties.items()}
        response_dict["_distance"] = o.metadata.distance
        out.append(response_dict)
    return out


def show(*args, **kwargs):
    print("@@@@", *args, **kwargs)


weaviate_version = "1.26.4"

client = weaviate.WeaviateClient(
    embedded_options=EmbeddedOptions(
        additional_env_vars={
            "ASYNC_INDEXING": "false",
            "DISABLE_TELEMETRY": "true",
            "DISK_USE_READONLY_PERCENTAGE": "98",
            "DISK_USE_WARNING_PERCENTAGE": "90",
            "ENABLE_MODULES": "backup-filesystem",
            # "LIMIT_RESOURCES": "true",
            "LOG_LEVEL": "warning",
            "MODULES_CLIENT_TIMEOUT": "10s",
            "PERSISTENCE_HNSW_MAX_LOG_SIZE": "500MiB",
            "PERSISTENCE_LSM_ACCESS_STRATEGY": "mmap",
            "PERSISTENCE_LSM_MAX_SEGMENT_SIZE": "20GiB",
            "QUERY_SLOW_LOG_ENABLED": "true",
            "QUERY_SLOW_LOG_THRESHOLD": "10s",
            "REINDEX_SET_TO_ROARINGSET_AT_STARTUP": "true",
            "BACKUP_FILESYSTEM_PATH": "/tmp/backups",
        },
        version=weaviate_version,
        port=8079,
    )
)


client.connect()

try:
    collection_name = "CollectionFoo"

    if client.collections.exists(collection_name):
        collection = client.collections.get(collection_name)
    else:
        collection = client.collections.create(
            name=collection_name,
            vector_index_config=Configure.VectorIndex.hnsw(
                distance_metric=VectorDistances.COSINE
            ),
            properties=[
                Property(name="item", data_type=DataType.TEXT),
                Property(name="price", data_type=DataType.NUMBER),
            ],
        )

        data_rows = [
            {
                "vector": [i / 256, 1 - i / 256],
                "properties": {"item": f"{i:03d}", "price": i},
            }
            for i in range(256)
        ]

        with collection.batch.dynamic() as batch:
            for data_row in data_rows:
                batch.add_object(**data_row)

    show(client.cluster.nodes(output="verbose"))

    query = [0.7, 0.7]

    # response = collection.query.near_vector(
    # near_vector=query,
    # limit=1,
    # return_metadata=MetadataQuery(distance=True),
    # filters=Filter.by_property("price").greater_than(0),
    # )
    # response_dict = response_to_dict(response, selecting_properties={"item"})
    # show(response_dict)

    query_batch = [query for _ in range(3)]

    def query_func(x):
        return response_to_dict(x, selecting_properties={"item"})

    batch_results = batch_search(
        collection,
        query_batch,
        search_kwargs=dict(
            limit=1,
            return_metadata=MetadataQuery(distance=True),
            filters=Filter.by_property("price").greater_than(0),
        ),
        query_fn=query_func,
        loader_kwargs={"batch_size": 100, "num_workers": 2},
        tqdm_kwargs={"mininterval": 1.0},
    )
    show(batch_results)

except:
    raise
finally:
    show("closing client...")
    client.close()
    show("closed client.")
