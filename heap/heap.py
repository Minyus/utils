import heapq


class MinHeap:
    def __init__(self, ls=None):
        ls = ls or []
        self.q = ls
        heapq.heapify(self.q)

    def heappush(self, x):
        heapq.heappush(self.q, x)

    def heappop(self):
        return heapq.heappop(self.q)

    def __getitem__(self, i):
        return self.q[i]

    def __repr__(self):
        return self.q.__repr__()


class MaxHeap:
    def __init__(self, ls=None):
        ls = ls or []
        for i in range(len(ls)):
            if isinstance(ls[0], tuple):
                ls[i] = (-ls[i][0], *ls[i][1:])
            else:
                ls[i] = -ls[i]
        self.q = ls
        heapq.heapify(self.q)

    def heappush(self, x):
        if isinstance(x, tuple):
            v = (-x[0], *x[1:])
        else:
            v = -x
        heapq.heappush(self.q, v)

    def heappop(self):
        v = heapq.heappop(self.q)
        if isinstance(v, tuple):
            return (-v[0], *v[1:])
        return -v

    def __getitem__(self, i):
        v = self.q[i]
        if isinstance(v, tuple):
            return (-v[0], *v[1:])
        return -v

    def __repr__(self):
        return self.q.__repr__()


if __name__ == "__main__":
    for h in [MinHeap([8, 7]), MaxHeap([7, 8])]:
        print(h)
        h.heappush(6)
        print(h)
        h.heappush(9)
        print(h)
        print(h.heappop())
        print(h)
        print(h.heappop())
        print(h)
        print(h[0])
        print("Done")
    for h in [MinHeap([(7, 100), (8, 200)]), MaxHeap([(7, 100), (8, 200)])]:
        print(h)
        h.heappush((6, 500))
        print(h)
        h.heappush((9, 600))
        print(h)
        print(h.heappop())
        print(h)
        print(h.heappop())
        print(h)
        print(h[0])
        print("Done")
