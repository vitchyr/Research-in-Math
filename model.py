import networkx
import random
import math

def f(d, d_mean, th):
    c = math.log(2)
    return 1 - math.e**(-c * (th * d / d_mean + (1.0 - th)))

def iterate(graph, th, edges=None):
    eid = random.randint(0, graph.number_of_edges() - 1)

    if edges is None:
        edges = graph.edges()

    edge = edges[eid]

    if random.random() < .5:
        x, y = edge
    else:
        y, x = edge

    z = x
    while z == x or z == y:
        z = random.randint(0, graph.number_of_nodes() - 1)

    d = graph.degree(z)

    if random.random() < f(d, graph.d_mean, th):
        graph.remove_edge(x, y)
        del edges[eid]

        graph.add_edge(x, z)
        edges.append((x, z))

    return edges

if __name__ == '__main__':
    n = 1000 
    m = 8000
    times = 10**6
    th = 0.5

    graph = networkx.MultiGraph(networkx.gnm_random_graph(n, m)) 
    graph.d_mean = 2 * float(graph.number_of_edges()) / graph.number_of_nodes()
    edges = None

    for i in range(times):
        edges = iterate(graph, th, edges)
