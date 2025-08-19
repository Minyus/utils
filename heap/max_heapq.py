import heapq


def max_heappush(q, x):
    """Define heappush for max heap"""
    if isinstance(x, tuple):
        v = (-x[0], *x[1:])
    else:
        v = -x
    heapq.heappush(q, v)


def max_heappop(q):
    """Define heappop for max heap"""
    v = heapq.heappop(q)
    if isinstance(v, tuple):
        return (-v[0], *v[1:])
    return -v


if __name__ == "__main__":
    q = []
    max_heappush(q, 5)
    max_heappush(q, 2)
    max_heappush(q, 4)
    print(max_heappop(q))
    print(max_heappop(q))
    print(max_heappop(q))
    q = []
    max_heappush(q, (5, 1))
    max_heappush(q, (2, 2))
    max_heappush(q, (4, 3))
    print(max_heappop(q))
    print(max_heappop(q))
    print(max_heappop(q))
