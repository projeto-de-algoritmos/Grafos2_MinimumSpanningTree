import sys, threading
from heapq import heappop, heappush
from mygraph import MyGraph
from collections import defaultdict

n_nodes, n_edges = map(int, input("Insira o número de nós e arestas: ").split())

edges = list()

results = defaultdict(lambda: 'any')
highest = defaultdict(lambda: -1)
to_check = defaultdict(list)
graph = defaultdict(list)

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

def make_graph(n_nodes, label):
    graph = MyGraph(graph_type='graph', size='20,11.25!', ratio='fill',label=label, fontsize=40)
    
    for v in range(1, n_nodes+1):
        graph.add_nodes(v)

    return graph

def make_graph_img(graph, img_name):
    graph.save_img(img_name)
    
    print(f"O grafo foi salvo em {img_name}.png!")

def dfs(a, depth, p):
    global edges
    global results
    global highest
    global graph

    if highest[a] != -1:
        return highest[a];

    minimum = depth
    highest[a] = depth

    for (w, a, b, i) in graph[a]:
        if i == p:
            continue

        nextt = dfs(b, depth + 1, i)

        if nextt <= depth:
            results[i] = 'at least one'
        else:
            results[i] = 'any'

        minimum = min(minimum, nextt)
        highest[a] = minimum

    return highest[a]

def main():
    global edges
    global results
    global highest
    global graph

    original_graph = make_graph(n_nodes, "Grafo Original")
    
    edges_in_mst_graph = make_graph(n_nodes, "Arestas em MSTs")

    edges_dict = dict()

    for i in range(n_edges):
        a, b, w = map(int, input('\tInsira dois nós e o peso da aresta que existe entre eles: ').split())
        edges.append((w, a-1, b-1, i))
        original_graph.link(a, b, str(w))
        edges_dict[i] = (w, a, b)

    make_graph_img(original_graph, "original_graph")

    edges = sorted(edges, key=lambda x: x[0])

    dsu = UDFS(n_nodes)

    i = 0
    while i < n_edges:
        counter = 0
        j = i
        while j < n_edges and edges[j][0] == edges[i][0]:
            if dsu.get_group(edges[j][1]) == dsu.get_group(edges[j][2]):
                results[edges[j][3]] = 'none'
            else:
                to_check[counter] = edges[j]
                counter += 1
            j += 1
            
        for k in range(counter):
            w, a, b, i = to_check[k]

            ra = dsu.get_group(a)
            rb = dsu.get_group(b)

            graph[ra].append((w, ra, rb, i))
            graph[rb].append((w, rb, ra, i))

        for k in range(counter):
            dfs(to_check[k][1], 0, -1)

        for k in range(counter):
            w, a, b, i = to_check[k]

            ra = dsu.get_group(a)
            rb = dsu.get_group(b)

            dsu.join(ra, rb)

            graph[ra] = list()
            graph[rb] = list()

            highest[ra] = -1
            highest[rb] = -1

        counter = 0
        i = j

    for i in range(n_edges):
        w, a, b = edges_dict[i]
        edges_in_mst_graph.link(a, b, results[i], w)

    make_graph_img(edges_in_mst_graph, "edges_in_mst")

if __name__ == "__main__":
    sys.setrecursionlimit(2**32//2-1)
    threading.stack_size(1 << 27)

    thread = threading.Thread(target=main)
    thread.start()
    thread.join()
