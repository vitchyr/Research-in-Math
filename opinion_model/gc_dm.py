import networkx as nx
import model

if __name__ == '__main__':
    n = 2000

    k_min = 0.5
    k_step = 0.25
    k_max = 2.5
    D = 3
    times = 5*10**0
    stats_size = 50
    alpha = 2

    outstring = 'k\tGC Size\n'
    print 'k\tGC Size'
    k = k_min
    while k <= k_max:
        print "Starting k = %f" % k

        gc_size_total = 0
        for j in xrange(stats_size):
            G = model.make_opinion_graph(n, .5 * n * k, D, alpha)

            for i in xrange(n*times):
                model.iterate(G)

            gc_size_total += nx.number_of_nodes(nx.connected_component_subgraphs(G)[0])

        outstring += '{0}\t{1}\n'.format(k, gc_size_total / float(stats_size))
        print '{0}\t{1}'.format(k, gc_size_total / float(stats_size))
        k += k_step

    filename = 'opGCSize_{0}n_{1}D_{2}alpha_{3}min_{4}max_{5}times_{6}size.dat'.format(n, D, alpha, k_min, k_max, times, stats_size)
    outfile = open(filename, 'w')
    outfile.write(outstring)
    outfile.close()
