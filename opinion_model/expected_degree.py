import networkx as nx
import model

def write_expected_deg(G, n, d_mean, D, times):
    #for obs_degrees,
    #key = degree
    #value = freq
    print "iterating"
    for i in xrange(times):
        model.iterate(G)

    print "storing degree informations"
    obs_degrees = {}
    for x in G.nodes_iter():
        if G.degree(x) in obs_degrees:
            obs_degrees[G.degree(x)] += 1
        else:
            obs_degrees[G.degree(x)] = 1

    outstring = "degree\tfrequency\n"
    for key in obs_degrees.iterkeys():
        outstring += "%s\t%d\n" % (key, obs_degrees[key])

    #save data
    print "saving data"
    outfile = open('expected_degree_{0}n_{1}k_{2}D.dat'.format(n, d_mean, D), 'w')
    outfile.write(outstring)
    outfile.close()

if __name__ == '__main__':
    n = 2000 
    d_mean = 4.0
    D = 3
    times = 10**6                               

    G = model.make_opinion_graph(n, 0.5 * d_mean * n, D)

    write_expected_deg(G, n, d_mean, D, times)
