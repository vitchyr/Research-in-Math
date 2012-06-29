import networkx as nx
import model

def write_expected_deg(G, n, d_mean, D):
    #key = opinion
    #value = degree
    obs_degrees = {}
    for x in G.nodes_iter():
        obs_degrees[G.node[x]['op'][0]] = G.degree(x)

    outstring = "opinion\tdegree\n"
    for key in obs_degrees.iterkeys():
        outstring += "%f\t%d\n" % (key, obs_degrees[key])

    #save data
    outfile = open('expected_degree_{0}n_{1}k_{2}D.dat'.format(n, d_mean, D), 'w')
    outfile.write(outstring)
    outfile.close()

if __name__ == '__main__':
    n = 2000 
    d_mean = 4.0
    D = 1

    G = model.make_graph(n, 0, D)
    model.construct(G, d_mean)

    write_expected_deg(G, n, d_mean, D)
