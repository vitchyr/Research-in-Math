import networkx
import matplotlib
import random

def d(G, x, y):
    vec_x = G.node[x]['op']
    vec_y = G.node[y]['op']

    sq_sum = 0.0

    for i in range(G.D):
        sq_sum += (vec_x[i] - vec_y[i])**2
        
    return sq_sum**.5        

def random_opinions(G):
    for v in G.nodes_iter():
        G.node[v]['op'] = []

        for i in range(G.D):
            G.node[v]['op'].append(random.random())

def iterate(G):
    if '_edges' not in G.__dict__:
        G._edges = G.edges()

    x, y = random.choice(G._edges)

    if random.random() < .5:
        x, y = y, x

    p = G.D**-.5
    d_xy = d(G, x, y)

    if random.random() > p * d(G, x, y):
        return

    z = x
    while z == x or z == y or G.has_edge(x, z):
        z = random.randint(0, G.number_of_nodes() - 1) 

    d_xz = d(G, x, z)

    if d_xy < d_xz and random.random() > d_xy / d_xz:
        return

    G.remove_edge(x, y) 
    G.add_edge(x, z)

    if x < y:
        G._edges.remove((x, y))
    else:
        G._edges.remove((y, x))

    if x < z:
        G._edges.append((x, z))
    else:
        G._edges.append((z, x))

def draw_graph(G):
    if G.D == 1:
        pass
    else:
        pos = {}
        for v in G.nodes_iter():
            pos[v] = G.node[v]['op']

        networkx.draw(G, pos)
        matplotlib.pyplot.show()

if __name__ == '__main__':
    n = 20 
    m = 40
    times = 10**4
    D = 2

    G = networkx.MultiGraph(networkx.gnm_random_graph(n, m))
    G.D = D
    random_opinions(G)

    for i in range(times):
        iterate(G)

    draw_graph(G)
