import heapq


class MinHeap(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        heapq.heapify(self)

    def heappush(self, x):
        heapq.heappush(self, x)

    def heappop(self):
        return heapq.heappop(self)


class MaxHeap(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(len(self)):
            self[i] = -self[i]
        heapq.heapify(self)

    def heappush(self, x):
        heapq.heappush(self, -x)

    def heappop(self):
        return -heapq.heappop(self)


if __name__ == "__main__":
    h = MinHeap([8, 7])
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
