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

def length(G, edge):
    vec_x = G.node[edge[0]]['op']
    vec_y = G.node[edge[1]]['op']
    return dn(vec_x, vec_y)

#returns c in Theorem 2
def k(G, m=0):
    total = 0.0

    for (u, u_data) in G.nodes_iter(True):
        for (v, v_data) in G.nodes_iter(True):
            if u < v:
                total += (dn(u_data['op'], v_data['op'])**2 + 1.0)**-1

    if m == 0:
        m = G.number_of_edges()

    G.k = m / total
    print G.k
    return G.k

#uses Newton's method to find k in Theorem 2
#finds the zero of the function:
#   f(c) = sum over all edges in K-n (c/(d(e)^2+c) - m
def k_num(G, tolerance, maxIter):
    print "Calculating k"
    k = k_num_helper(1.0, G, tolerance, maxIter, 1)
    print k
    return k

def k_num_helper(last, G, tolerance, maxIter, currentIter):
    if currentIter > maxIter:
        return last
    new = last - (getPSum(G, last) - G.number_of_edges())/getDPSum(G, last)
    if abs(new - last) < tol:
        return new
    else:
        return k_num_helper(new, G, tolerance, maxIter, currentIter + 1)

#gives the sum of the P(e) for all edges in the complete
#graph K_n. Finds f(last) + m
def getPSum(G, last):
    total = 0.0
    for v in G.node_iter():
        for u in G.node_iter():
            if v < u:
                total += last/(d(G, u, v)**2 + last)
    return total

#gives the sum of the d/dk(P(e)) for all edges in the complete
#graph K_n, where k is the constant. In otherwords, finds
#d/dc(f(last))
def getDPSum(G, last):
    total = 0.0
    for v in G.node_iter():
        for u in G.node_iter():
            if v < u:
                total += d(G, u, v)**2/(d(G, u, v)**2 + last)
    return total

def random_opinions(G):
    for v in G.nodes_iter():
        G.node[v]['op'] = []

        for i in range(G.D):
            G.node[v]['op'].append(random.random())

def construct(G, d_mean):
    k(G, .5 * G.number_of_nodes() * d_mean) 
    for (u, u_data) in G.nodes_iter(True):
        for (v, v_data) in G.nodes_iter(True):

            if(u < v and 
                random.random() <
                G.k * (dn(u_data['op'], v_data['op'])**2 + 1.0)**-1):
                G.add_edge(u, v)

def reconstruct(G, d_mean):
    G.remove_edges_from(G.edges())
    construct(G, d_mean)

def iterate(G):
    G._edges = G.edges()

    x, y = random.choice(G._edges)

    if random.random() < .5:
        x, y = y, x

    #For geometric distance, use: 
    #p = G.D**-.5
    #For step distance, use:
    p = G.D
    d_xy = d(G, x, y)

    if random.random() > p * d(G, x, y):
        return

    z = x
    if G.degree(x) == G.number_of_nodes() - 1:
        return
    
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

def make_graph(n, m, D):
    G = networkx.gnm_random_graph(n, m)
    G.D = D
    random_opinions(G)
    return G

if __name__ == '__main__':
    n = 50000
    k = 4
    times = 10**7
    D = 1

    G = make_graph(n, .5 * n * k, D)

    for i in range(times):
        iterate(G)

    write_deg(G, .04)
    #draw_graph(G)
