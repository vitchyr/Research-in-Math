import networkx as nx
import model
import math

def write_edge_existence(G, iterations, times, n, d_mean, D):
    #keeps track of how often a specific edge appears
    #key = edge
    #value = frequency
    edge_obs_freq = {}

    for i in xrange(times):
        if i % (times/10) == 0:
            print "%d times" % i

        #Method 1
        remake_graph(G)

        #Method 2
        #model.reconstruct(G, d_mean)
        
        for j in xrange(iterations):
            model.iterate(G)

        for edge in G.edges_iter():
            if edge in edge_obs_freq:
                edge_obs_freq[edge] += 1
            else:
                edge_obs_freq[edge] = 1

    #normalize observed frequencies
    for key in edge_obs_freq.iterkeys():
        edge_obs_freq[key] = float(edge_obs_freq[key]) / times

    model.k(G)
    edge_expected_freq = expected_edge_freq(G.number_of_nodes())

    outstring = "edge\tdistance\tobs_freq\texpected_freq\n"
    for key in edge_obs_freq.iterkeys():
        outstring += "%s\t%f\t%f\t%f\n" % (key, model.length(G, key), edge_obs_freq[key],
                                       edge_expected_freq[key])

    #save data
    outfile = open('edgeExistence_{0}n_{1}k_{2}d_{3}times_{4}iterations.dat'.format(n, d_mean, D, times, iterations), 'w')
    outfile.write(outstring)
    outfile.close()

def expected_edge_freq(n):
    completeG = nx.complete_graph(n)
    edge_expected_freq = {}
    for edge in completeG.edges_iter(): 
         edge_expected_freq[edge] = G.k/(model.length(G, edge)**2+1)
                 
    return edge_expected_freq

#this is to preserve the opinions of vertices
def remake_graph(G):
    H = model.make_graph(n, d_mean * n / 2, D) #seeded with new edge list
    G.remove_edges_from(G.edges())
    G.add_edges_from(H.edges())

#There are two Methods to add edges:
#   1. By using nx.gnm_random   (Must iterate for graph to reach steady state)
#   2. By using model.construct (Theorem 2 - construct a graph at the steady state)
#This is a test of Theorem 2, so Method 1 is used    
if __name__ == '__main__':
    n = 50 
    d_mean = 2.0
    D = 1
    iterations = 1000
    times = 1000

    #Method 1
    G = model.make_graph(n, d_mean * n / 2, D)

    #Method 2
    #G = model.make_graph(n, 0, D)
    #model.construct(G, d_mean)
    
    write_edge_existence(G, iterations, times, n, d_mean, D)
