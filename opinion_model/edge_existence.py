import networkx as nx
import model
import math

def write_edge_existence(G, iterations, times, bin_decimal_places, n, d_mean, D):
    completeG = nx.complete_graph(G.number_of_nodes())

    #keeps track of how often an edge of a certain distance appears
    distance_obs_freq = {}

    for i in xrange(times):
        if i % (times/10) == 0:
            print "%d times" % i
            
        for j in xrange(iterations):
            model.iterate(G)

        edgeList = G.edges()
        for node_pair in G.edges_iter():
            if node_pair in edgeList:
                node1 = edgeList[edgeList.index(node_pair)][0]
                node2 = edgeList[edgeList.index(node_pair)][1]
                #distances are rounded to bin_decimal_places decimal places
                distance = round(model.d(G, node1, node2), bin_decimal_places)
                if distance in distance_obs_freq:
                    distance_obs_freq[distance] += 1.0/times/G.number_of_edges()
                else:
                    distance_obs_freq[distance] = 1.0/times/G.number_of_edges()

    distance_expected_freq = expected_distance_freq(G, distance_obs_freq.keys(),
                                         bin_decimal_places)


    outstring = "distance\tobs_freq\texpected_freq\n"
    for key in distance_obs_freq.iterkeys():
        outstring += "%f\t%f\t%f\n" % (key, distance_obs_freq[key],
                                       distance_expected_freq[key]*times)

    #save data
    outfile = open('edgeExistence_{0}n_{1}k_{2}d_{3}times_{4}iterations.dat'.format(n, d_mean, D, times, iterations), 'w')
    outfile.write(outstring)
    outfile.close()

def expected_distance_freq(G, distance_keys, bin_decimal_places):
    distance_expected_freq = {}
    for distance in distance_keys: 
        #uses Theorem 2
        #to get a binned expected frequency, integrate c/(d^2+1) over the bin
        #this is given by c*(arctan(upper) - arctan(lower)
        #distance_expected_freq[distance] = G.k*(math.atan(distance + 10**-bin_decimal_places) - math.atan(distance))/2
        distance_expected_freq[distance] = G.k/(distance**2+1)
                 
    return distance_expected_freq

if __name__ == '__main__':
    n = 10 
    d_mean = 4.0
    D = 1
    iterations = 1000
    times = 100
    bin_decimal_places = 2

    G = model.make_graph(n, 0, D)
    model.construct(G, d_mean)
    write_edge_existence(G, iterations, times, bin_decimal_places, n, d_mean, D)
