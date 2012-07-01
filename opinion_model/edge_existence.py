import networkx as nx
import model

def write_edge_existence(G, iterations, times, n, d_mean, D, sample_rate, throw_away):
    #put this first so that the "Exiting..." occurs before
    #any time is spent on lots of computing
    if 'c' in G.__dict__:
        edge_expected_freq = expected_edge_freq(G)
    else:
       print "G.c not initalized. Exiting..."
       return

    #edge_obs_freq keeps track of how often a specific edge appears
    #key = edge
    #value = frequency
    edge_obs_freq = {}
    print "Collecting data on edge existence"
    for i in xrange(times):
        if i % (times/10) == 0:
            print "%d percent" % (100 * i / times)
 
        #Method 1
        remake_graph(G)

        #Method 2
        #model.reconstruct(G, d_mean)

        number_of_samples = 0

        for j in xrange(iterations + throw_away):
            if j >= throw_away and j % sample_rate == 0:
                number_of_samples += 1

                for edge in G.edges_iter():
                    if edge in edge_obs_freq:
                        edge_obs_freq[edge] += 1
                    else:
                        edge_obs_freq[edge] = 1

            model.iterate(G)

    #normalize observed frequencies
    for key in edge_obs_freq.iterkeys():
        edge_obs_freq[key] = float(edge_obs_freq[key]) / (number_of_samples*times)

    #save the data
    outstring = "edge\tdistance\tobs_freq\texp_freq\n"
    for key in edge_obs_freq.iterkeys():
        outstring += "%s\t%f\t%f\t%f\n" % (key, model.length(G, key), 
            edge_obs_freq[key], edge_expected_freq[key])

    outfile = open('edgeExistence_{0}n_{1}k_{2}d_{3}times_{4}iterations.dat'.format(n, d_mean, D, times, iterations), 'w')
    outfile.write(outstring)
    outfile.close()

def expected_edge_freq(G):
    edge_expected_freq = {}
    for u in G._nodes:
        for v in G._nodes:
            if u < v:
                freq = G.c/(model.distance(G, u, v)**2+G.c)
                #for when edge_expected_freq[key] since the key can be
                #either (u, v) or (v, u)
                edge_expected_freq[(u, v)] = freq
                edge_expected_freq[(v, u)] = freq
    return edge_expected_freq

#this is to preserve the opinions of vertices
def remake_graph(G):
    if '_edges' not in G.__dict__:      #to save computing time since 
        G.remove_edges_from(G._edges)   #G.edges() takes a lot
    else:
        G.remove_edges_from(G.edges())
    model.add_random_edges(G, G.m)

#There are two Methods to add edges:
#   1. By using nx.gnm_random   (Must iterate for graph to reach steady state)
#   2. By using model.construct (Theorem 2 - construct a graph at the steady state)
#This is a test of Theorem 2, so Method 1 is used    
if __name__ == '__main__':
    n = 50 
    d_mean = 2.0
    D = 3
    iterations = 10**4
    times = 100
    sample_rate = 100
    throw_away = 10**3

    iterations_for_getting_C = 100

    #Method 1
    G = model.make_opinion_graph(n, (d_mean * n) / 2, D)

    #Method 2
    #G = model.make_graph(n, 0, D)
    #model.construct(G, d_mean)

    #required for expected calculation
    G.c = model.getC(G, iterations_for_getting_C)
    #G.c = 0.0001778  
    write_edge_existence(G, iterations, times, n, d_mean, D, sample_rate, throw_away)
