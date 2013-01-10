import networkx as nx
import model

if __name__ == '__main__':
    n_min = 200
    n_step = 100
    n_max = 1000

    k = 4
    D = 1
    times = 5*10**4
    stats_size = 1
    alpha = 2

    outstring = 'N\tMean Pair-Wise Distance\n'
    print 'Working on ',
    print 'opPairwise_{0}k_{1}D_{2}alpha_{3}min_{4}max_{5}times_{6}size.dat'.format(k, D, alpha, n_min, n_max, times, stats_size)
    print 'N\tMean Pair-Wise Distance'
    for n in xrange(n_min, n_max + n_step, n_step):
        print "Starting n = %d" % n
        pairwise_total = 0
        for j in xrange(stats_size):
            G = model.make_opinion_graph(n, .5 * n * k, D, alpha)

            for i in xrange(n*times):
                model.iterate(G)

            giant_component = nx.connected_component_subgraphs(G)[0]
            iter_pw_distance = 0        #diameter may not be diameter
            for vertex_one in giant_component.nodes():
                for vertex_two in giant_component.nodes():
                    if vertex_one == vertex_two:
                        break
                    iter_pw_distance += nx.shortest_path_length(
                        giant_component, vertex_one, vertex_two)


            buf = giant_component.number_of_nodes()
            pairs = buf * (buf - 1) / 2
            pairwise_total += float(iter_pw_distance) / pairs

        outstring += '{0}\t{1}\n'.format(n, pairwise_total / float(stats_size))
        print '{0}\t{1}'.format(n, pairwise_total / float(stats_size))

    filename = 'opPairwise_{0}k_{1}D_{2}alpha_{3}min_{4}max_{5}times_{6}size.dat'.format(k, D, alpha, n_min, n_max, times, stats_size)
    outfile = open(filename, 'w')
    outfile.write(outstring)
    outfile.close()
