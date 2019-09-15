from heapq import heappop, heappush

class UDFS:

    def __init__(self, n):
        self.n = n

        # index is the node
        self.parents = [i for i in range(n)]
        self.ranks = [0 for i in range(n)]

    def __str__(self):
        '''
        Group -> Node
        '''
        return '\n'.join(f'{e} -> {i}' for i, e in enumerate(self.parents))

    def get_group(self, a):
        if a == self.parents[a]:
            return a

        # Side effect for balancing the tree
        self.parents[a] = self.get_group(self.parents[a])

        return self.parents[a]

    def is_parent(self, n):
        return n == self.get_group(n)

    def is_same_group(self, a, b):
        return self.get_group(a) == self.get_group(b)

    def join(self, a, b):
        parent_a = self.get_group(a)
        parent_b = self.get_group(b)

        if self.ranks[parent_a] > self.ranks[parent_b]:
            self.parents[parent_b] = parent_a
        else:
            self.parents[parent_a] = parent_b

            self.ranks[parent_b] += int(
                self.ranks[parent_a] == self.ranks[parent_b]
            )

    def count(self):
        '''
        Returns number of groups
        '''
        count = 0
        for n in range(self.n):
            count += self.is_parent(n)

        return count

n_nodes, n_edges = map(int, input().split())

edges = []
for i in range(n_edges):
    a, b, w = map(int, input().split())
    heappush(edges, (w, a-1, b-1, i))

results = ['none' for _ in range(n_edges)]
dsu = UDFS(n_nodes)
count = 0

minimum, a, b, i = heappop(edges)
dsu.join(a, b)
count += 1
results[i] = 'any'  # minimum edge

prev = (i, minimum)
for _ in range(n_edges-1):
    if count == (n_nodes - 1): # Everybody is connected
        break

    w, a, b, i = heappop(edges)

    if w == prev[1]:
        results[i] = 'at least one'
        results[prev[0]] = 'at least one'
    elif not dsu.is_same_group(a, b):
        dsu.join(a, b)
        results[i] = 'any'
        count += 1

    prev = (i, w)

print('\n'.join(results))
