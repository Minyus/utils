import shutil
import lancedb
import torch


class SearchDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        tbl,
        query_batch,
        search_kwargs={},
        query_fn=None,
    ):
        self.tbl = tbl
        self.query_batch = query_batch
        self.search_kwargs = search_kwargs
        self.query_fn = query_fn

    def __len__(self):
        return len(self.query_batch)

    def __getitem__(self, idx):
        query = self.query_batch[idx]
        result = tbl.search(query, **self.search_kwargs)
        if self.query_fn is not None:
            result = self.query_fn(result)
        return result


def batch_search(
    tbl,
    query_batch,
    search_kwargs={},
    query_fn=None,
    loader_kwargs={},
):
    dataset = SearchDataset(
        tbl,
        query_batch,
        search_kwargs=search_kwargs,
        query_fn=query_fn,
    )
    loader_kwargs.setdefault("collate_fn", lambda x: x)
    data_loader = torch.utils.data.DataLoader(dataset, **loader_kwargs)

    out = []
    for mini_batch in data_loader:
        out.extend(mini_batch)
    return out


if __name__ == "__main__":

    uri = "/tmp/sample-lancedb"
    shutil.rmtree(uri, ignore_errors=True)
    db = lancedb.connect(uri)
    data = [
        {"vector": [0, -1], "item": "foo", "price": 10.0},
        {"vector": [0, 1], "item": "bar", "price": 20.0},
        {"vector": [-1, 0], "item": "baz", "price": 30.0},
    ]
    tbl = db.create_table("my_table", data=data)
    query = [0.7, 0.7]

    query_batch = [query for _ in range(3)]
    batch_results = batch_search(
        tbl,
        query_batch,
        search_kwargs={},
        query_fn=lambda x: x.metric("cosine")
        .where("price < 25", prefilter=True)
        .select(["item"])
        .limit(1)
        .to_list(),
        loader_kwargs={},
    )
    print(batch_results)
