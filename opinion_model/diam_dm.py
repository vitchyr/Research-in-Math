import networkx
import model

if __name__ == '__main__':
    n_min = 200
    n_step = 25
    n_max = 800

    k = 4
    D = 1
    times = 5*10**4
    stats_size = 50

    outstring = ''
    for n in xrange(n_min, n_max, n_step):

        diam_total = 0
        for j in xrange(stats_size):
            G = model.make_graph(n, .5 * n * k, D)

            for i in xrange(times):
                model.iterate(G)

            gc = networkx.connected_component_subgraphs(G)[0]
            diam_total += networkx.diameter(gc)

        outstring += '{0}\t{1}\n'.format(n, diam_total / float(stats_size))

    filename = 'opdiameter_{0}_{1}.dat'.format(k, D)
    outfile = open(filename, 'w')
    outfile.write(outstring)
