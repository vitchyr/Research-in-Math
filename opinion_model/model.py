import networkx as nx
import matplotlib
import random

def distance(G, u, v):
    total = 0.0

    if G.looping:
        for i in range(G.D):
            total += min(abs(u[i] - v[i]), u[i] + 1 - v[i],
                v[i] + 1 - u[i])
    else:
        for i in range(G.D):
            total += abs(u[i] - v[i])
        
    return total

def length(G, edge):
    return distance(G, edge[0], edge[1])

def iterate(G):
    if '_edges' not in G.__dict__:
        G._edges = G.edges()

    x, y = random.choice(G._edges)

    if random.random() < .5:
        x, y = y, x

    if G.degree(x) == G.n - 1:
        return

    #For geometric distance, use: 
    #p = G.D**-.5
    #For step distance, use:
    p = 1.0/G.D
    d_xy = distance(G, x, y)

    if random.random() > p * distance(G, x, y):
        return

    z = x
    while z == x or z == y or G.has_edge(x, z):
        z = random.choice(G._nodes)

    d_xz = distance(G, x, z)
    
    if d_xy < d_xz and random.random() > d_xy / d_xz:
        return

    G.remove_edge(x, y) 
    G.add_edge(x, z)

    if (x,y) in G._edges:
        G._edges.remove((x, y))
    else:
        G._edges.remove((y, x))

    #not sure if this is correct. We might want to always append (x,z)
    #since edge_existence.remake_graph deletes edges by using ._edges
    if (x,z) in G._edges:
        G._edges.append((x, z))
    else:
        G._edges.append((z, x))

def draw_graph(G):
    pos = {}
    if G.D == 1: #draws along a circle
        radius = min(1.0, math.log(G.n))
        for v in G.nodes_iter():
            opinion = list(v)[0]
            pos[v] = [radius * math.cos(opinion), radius * math.sin(opinion)]
    else:
        if G.D > 2:
            print "Drawing based on first two opinions"
        for v in G.nodes_iter():
            pos[v] = list(v)[:2]
    nx.draw(G, pos)
    matplotlib.pyplot.show()

#******** Methods for getting G.k (Theorem 2 ********

#uses bisection method to find c values, and averages them.
def getC(G, m, iterations, tol, start):
    print "Calculating G.c (Theorem 2)"
    G.m = m

    c_values = []
    for i in xrange(iterations):

        if iterations > 9 and i % (iterations/10) == 0:
            print "%d percent" % (100 * i / iterations)

        H = make_opinion_graph(G.n, G.m, G.D, G.looping)
        c_values.append(bisect(getPSumMinusM, H, 0.0, start, tol)) 

    c = sum(c_values)/len(c_values)
    print c
    return c

def bisect(f, G, left, right, tol ):
    a = left
    b = right
    currentIter = 0
    while True:
        c=(a+b)/2.0
        if( b-c < tol ):
            return c

        fGb = f(G, b)
        fGc = f(G, c)

        if( fGb > 0 and fGc <0 or fGb <0 and fGc >0 ):
            a=c
        else:
            b=c
        currentIter += 1
        print c

#gives the sum of the P(e) for all edges in the complete
#graph K_n minus m
def getPSumMinusM(G, last):
    total = 0.0

    for v in G.nodes_iter():
        for u in G.nodes_iter():
            if v[0] < u[0]:
                total += float(last)/(distance(G, u, v)**2 + last)

    return total - G.m

#******** Methods for adding edges ********

def construct(G, param, param_name):
    if param_name == 'k_mean':
        c = getC(G, 100, .5 * G.number_of_nodes() * param) 
    elif param_name == 'c':
        c = param
    else:
        print('incorrect param_name to construct!')
        return

    for u in G.nodes_iter():
        for v in G.nodes_iter():

            if(u[0] < v[0] and 
                random.random() <
                c / (distance(G, u, v)**2 + c)):
                G.add_edge(u, v)

def reconstruct(G, k_mean):
    G.remove_edges_from(G.edges())
    construct(G, k_mean)

#******** Graph creation - Version 1 ********
def make_graph(n, m, D):
    G = nx.gnm_random_graph(n, m)
    G.D = D
    random_opinions(G)
    return G

def random_opinions(G):
    for v in G.nodes_iter():
        G.node[v]['op'] = []

        for i in range(G.D):
            G.node[v]['op'].append(random.random())

#******** Graph creation - Version 1 ********

#Nodes are tuples that represent their opinion vector
#Access the ith opinion by using node[i]
def make_opinion_graph(n, m, D, looping=False):
    G = nx.Graph()
    G.D = D
    G.n = n
    G.m = m
    G.looping = looping

    nodeList = []
    for i in xrange(n):
        node = []
        for j in xrange(D):
            node.append(random.random())
        nodeList.append(tuple(node))
    G.add_nodes_from(nodeList)
    G._nodes = G.nodes()
    add_random_edges(G, m)
    return G

def add_random_edges(G, m):
    edges_added = 0
    while edges_added < m:
        u = random.choice(G._nodes)
        v = random.choice(G._nodes)
        while u == v:
            v = random.choice(G._nodes)
        if not G.has_edge(u, v):
            #(u, v) vs. (v, u) doesn't matter because networkx doesn't
            #sort .edges() if they're tuples
            #plus, there's a check in iterate ((x,y) in G._edges:) that
            #makes sure the correct one is removed
            G.add_edge(u, v)
            edges_added += 1
    G._edges = G.edges()

def mean_distance(G):
    total = 0.0

    for edge in G.edges_iter():
        total += distance(G, *edge)

    return total / G.number_of_edges()

if __name__ == '__main__':
    n = 2000 

    for D in (1, 2,3):
        G = make_opinion_graph(n, 0, D, True)
        c= getC(G, 4000, 1, 1e-8, 1e-2)
        construct(G, c, 'c')
        print G.number_of_edges()
