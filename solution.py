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
        return self.get_group(self.a) == self.get_group(self.b)

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

g = UDFS(10)
g.join(1, 4)
g.join(1, 2)
g.join(3, 4)
g.join(0, 9)
g.join(9, 3)
g.join(3, 9)
g.join(5, 2)
g.join(0, 7)
g.join(2, 8)
g.join(6, 2)
g.join(0, 7)
g.join(2, 1)
g.join(9, 9)
g.join(6, 7)
g.join(1, 4)

print(g)
print('Grupos:', g.count())
