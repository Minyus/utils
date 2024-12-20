import shutil
import lancedb
import torch

try:
    from tqdm import tqdm
except Exception:

    def tqdm(*args, **kwargs):
        return args[0]


def identity_func(x):
    return x


class LanceDBSearchDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        table,
        query_batch,
        search_kwargs={},
        query_fn=None,
    ):
        self.table = table
        self.query_batch = query_batch
        self.search_kwargs = search_kwargs
        self.query_fn = query_fn

    def __len__(self):
        return len(self.query_batch)

    def __getitem__(self, idx):
        query = self.query_batch[idx]
        result = self.table.search(query, **self.search_kwargs)
        if self.query_fn is not None:
            result = self.query_fn(result)
        return result


def batch_search(
    table,
    query_batch,
    search_kwargs={},
    query_fn=None,
    loader_kwargs={},
    tqdm_kwargs={},
):
    dataset = LanceDBSearchDataset(
        table,
        query_batch,
        search_kwargs=search_kwargs,
        query_fn=query_fn,
    )
    loader_kwargs.setdefault("collate_fn", identity_func)
    loader_kwargs.setdefault(
        "multiprocessing_context", "spawn" if loader_kwargs.get("num_workers") else None
    )
    data_loader = torch.utils.data.DataLoader(dataset, **loader_kwargs)
    if tqdm_kwargs is not None:
        data_loader = tqdm(data_loader, **tqdm_kwargs)

    out = []
    for mini_batch in data_loader:
        out.extend(mini_batch)
    return out


def query_func(x):
    return (
        x.metric("cosine")
        .where("price > 0", prefilter=True)
        .select(["item"])
        .limit(1)
        .to_list()
    )


if __name__ == "__main__":

    uri = "/tmp/sample-lancedb"
    shutil.rmtree(uri, ignore_errors=True)
    db = lancedb.connect(uri)
    data = [
        {"vector": [-1, 0], "item": "foo", "price": -1.0},
    ]
    table = db.create_table("my_table", data=data)
    print(f"{table.count_rows()=}")

    data = [
        {"vector": [i / 256, 1 - i / 256], "item": f"{i:03d}", "price": i}
        for i in range(256)
    ]
    table.add(data, mode="append")
    print(f"{table.count_rows()=}")

    table.create_index(
        metric="cosine",
        num_partitions=2,
        num_sub_vectors=1,
        index_cache_size=2,
    )
    query = [0.7, 0.7]

    query_batch = [query for _ in range(3)]

    batch_results = batch_search(
        table,
        query_batch,
        search_kwargs={},
        query_fn=query_func,
        loader_kwargs={"batch_size": 1, "num_workers": 2},
        tqdm_kwargs={"mininterval": 1.0},
    )
    print(batch_results)
