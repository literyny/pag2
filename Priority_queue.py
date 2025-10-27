import bisect

class Priority:
    def __init__(self, f=lambda x: x):
        self.L = []
        self.f = f
    def append(self, item):
        bisect.insort(self.L, (self.f(item), item)) # wyszukuje w czasie O(log n) miejsce, gdzie należy wstawić element
    def __len__(self):
        return len(self.L)
    def extend(self, items):
        for item in items:
            self.append(item)
    def pop(self):
        return self.L.pop()[1] # największy priorytet na początku listy
    def smallest(self):
        return self.L.pop(0)[1] # najmniejszy priorytet na początku listy