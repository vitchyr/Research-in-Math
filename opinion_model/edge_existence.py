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
        #uses Theorem 2
        #to get a binned expected frequency, integrate c/(d^2+1) over the bin
        #this is given by c*(arctan(upper) - arctan(lower)
        #distance_expected_freq[distance] = G.k*(math.atan(distance + 10**-bin_decimal_places) - math.atan(distance))/2
        edge_expected_freq[edge] = G.k/(model.length(G, edge)**2+1)
                 
    return edge_expected_freq

if __name__ == '__main__':
    n = 10 
    d_mean = 4.0
    D = 1
    iterations = 100
    times = 1000

    G = model.make_graph(n, 0, D)
    model.construct(G, d_mean)
    write_edge_existence(G, iterations, times, n, d_mean, D)
