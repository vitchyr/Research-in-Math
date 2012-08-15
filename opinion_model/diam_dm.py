import networkx as nx
import model

if __name__ == '__main__':
    n_min = 200
    n_step = 500
    n_max = 4700

    k = 4
    D = 2
    times = 5*10**0
    stats_size = 5
    alpha = 1

    outstring = 'N\tDiameter\n'
    print 'N\tDiameter'
    for n in xrange(n_min, n_max + n_step, n_step):
        print "Starting n = %d" % n
        diam_total = 0
        for j in xrange(stats_size):
            G = model.make_opinion_graph(n, .5 * n * k, D, alpha)

            for i in xrange(n*times):
                model.iterate(G)

            subgraphs = nx.connected_component_subgraphs(G)
            max_diameter = 0        #diameter may not be diameter
            for SG in subgraphs:    #of largest connected subgraph
                if SG.number_of_nodes() < 2:
                    break
                diameter = nx.diameter(SG)
                if diameter > max_diameter:
                    max_diameter = diameter

            diam_total += max_diameter

        outstring += '{0}\t{1}\n'.format(n, diam_total / float(stats_size))
        print '{0}\t{1}'.format(n, diam_total / float(stats_size))

    filename = 'opDiameter_{0}k_{1}D_{2}alpha_{3}min_{4}max_{5}times_{6}size.dat'.format(k, D, alpha, n_min, n_max, times, stats_size)
    outfile = open(filename, 'w')
    outfile.write(outstring)
    outfile.close()
