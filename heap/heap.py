import heapq


class MinHeap(list):
    def __init__(self, ls=[]):
        super().__init__(ls)
        heapq.heapify(self)

    def heappush(self, x):
        heapq.heappush(self, x)

    def heappop(self):
        return heapq.heappop(self)


class MaxHeap(list):
    def __init__(self, ls=[]):
        for i in range(len(ls)):
            if isinstance(ls[0], tuple):
                ls[i] = (-ls[i][0], *ls[i][1:])
            else:
                ls[i] = -ls[i]
        super().__init__(ls)
        heapq.heapify(self)

    def heappush(self, x):
        if isinstance(x, tuple):
            v = (-x[0], *x[1:])
        else:
            v = -x
        heapq.heappush(self, v)

    def heappop(self):
        v = heapq.heappop(self)
        if isinstance(v, tuple):
            return (-v[0], *v[1:])
        return -v


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
        print("Done")
