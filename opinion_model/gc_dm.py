import networkx
import model

if __name__ == '__main__':
    k_min = 2.7
    k_step = .1
    k_max = 3.2

    n = 2000
    D = 1
    stats_size = 10

    outstring = 'mean degree\tGC size\n'
    k = k_min
    
    while k <= k_max:
        print 'k = {0}'.format(k)

        gc_total = 0
        G = model.make_opinion_graph(n, 0, D)
        model.construct(G, k, 'k_mean')
        c = G.c
        for j in xrange(stats_size):
            G = model.make_opinion_graph(n, 0, D)
            model.construct(G, c, 'c')

            gc = networkx.connected_components(G)[0]
            gc_total += len(gc) / float(n)

        outstring += '{0}\t{1}\n'.format(k, gc_total / float(stats_size))
        print '{0}\t{1}\n'.format(k, gc_total / float(stats_size))
        k += k_step

    filename = 'opgc_{0}_{1}_{2}_{3}_{4}.dat'.format(n, D, k_min, k_step, k_max)
    outfile = open(filename, 'w')
    outfile.write(outstring)
    outfile.close()
