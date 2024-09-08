import weaviate
from weaviate.embedded import EmbeddedOptions
from weaviate.classes.config import Configure, Property, DataType, VectorDistances
from weaviate.classes.query import Filter, MetadataQuery

import torch

import socket
from contextlib import closing


def check_port_used(host="127.0.0.1", port=80, timeout=0.1):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port))


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
        collection_name,
        query_batch,
        search_kwargs={},
        query_fn=None,
    ):
        self.collection_name = collection_name
        self.collection = None
        self.query_batch = query_batch
        self.search_kwargs = search_kwargs
        self.query_fn = query_fn

    def __len__(self):
        return len(self.query_batch)

    def __getitem__(self, idx):
        if self.collection is None:
            client = get_client_at_open_port()
            self.collection = get_collection(client, self.collection_name)
        query = self.query_batch[idx]
        response = self.collection.query.near_vector(
            near_vector=query, **self.search_kwargs
        )
        if self.query_fn is not None:
            response = self.query_fn(response)
        return response

    def __del__(self):
        self.client.close()


def batch_search(
    collection_name,
    query_batch,
    search_kwargs={},
    query_fn=None,
    loader_kwargs={},
    tqdm_kwargs={},
):
    dataset = WeaviateSearchDataset(
        collection_name,
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


def get_client(port=8079, grpc_port=50060):
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
            port=port,
            grpc_port=grpc_port,
        )
    )

    client.connect()

    return client


def get_client_at_open_port(port=8079, grpc_port=50060, n_try=10):
    while check_port_used(port=port):
        port += 1
    while check_port_used(port=grpc_port):
        grpc_port += 1
    for i in range(n_try):
        try:
            client = get_client(port=port, grpc_port=grpc_port)
        except Exception:
            if i >= (n_try - 1):
                raise
            else:
                show(f"{port} or {grpc_port} not available.")
                port += 1
                grpc_port += 1

    return client


def get_collection(client, collection_name="CollectionFoo"):

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
    return collection


def query_func(x):
    return response_to_dict(x, selecting_properties={"item"})


if __name__ == "__main__":
    client = get_client_at_open_port()
    show(client.cluster.nodes(output="verbose"))
    client.close()

    query = [0.7, 0.7]

    query_batch = [query for _ in range(10000)]

    collection_name = "CollectionFoo"

    batch_results = batch_search(
        collection_name,
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
