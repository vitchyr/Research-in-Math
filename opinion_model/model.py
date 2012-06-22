import networkx
import matplotlib
import random

def dn(vec_x, vec_y):
    D = len(vec_x)
    total = 0.0

    for i in range(D):
        total += abs(vec_x[i] - vec_y[i])
        
    return total

def d(G, x, y):
    vec_x = G.node[x]['op']
    vec_y = G.node[y]['op']

    return dn(vec_x, vec_y)

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

def write_deg(G, dist_step):
    dist_data = []
    deg_data = []

    for v, deg in G.degree_iter():
        dist = dn(G.node[v]['op'], [.5]*G.D)
        dist_data.append(dist)
        deg_data.append(deg)

    import numpy
    bins = []
    dist = 0.0

    while dist < .5 * G.D + .001:
        bins.append(dist)
        dist += dist_step

    bins_np = numpy.array(bins)
    bin_indices = numpy.digitize(dist_data, bins_np)
    histogram = numpy.histogram(dist_data, bins_np)[0]

    mean_degree_data = [0.0] * (len(bins) - 1)
    for i in range(0, len(dist_data) - 1):
        mean_degree_data[bin_indices[i] - 1] += float(deg_data[i]) /\
            histogram[bin_indices[i] - 1] 

    outstring = ''
    for i in range(0, len(bins) - 1):
        outstring += '{0}\t{1}\n'.format(bins[i], mean_degree_data[i])

    k = 2 * G.number_of_edges() / G.number_of_nodes()
    outfile = open('opdegdist_{0}_{1}.dat'.format(k, G.D), 'w')
    outfile.write(outstring)

def make_graph(n, m, D):
    G = networkx.gnm_random_graph(n, m)
    G.D = D
    random_opinions(G)
    return G

if __name__ == '__main__':
    n = 1000 
    k = 4
    times = 10**6
    D = 3

    G = make_graph(n, .5 * n * k, D)

    for i in range(times):
        iterate(G)

    write_deg(G, .1)
    #draw_graph(G)
