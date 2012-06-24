import networkx
import model

if __name__ == '__main__':
    k_min = .6
    k_step = .2
    k_max = 2.0

    n = 400
    D = 3
    times = 0*5*10**4
    stats_size = 50

    outstring = ''
    k = k_min
    
    while k < k_max + .01:
        print 'k = {0}'.format(k)

        gc_total = 0
        for j in xrange(stats_size):
            G = model.make_graph(n, .5 * n * k, D)

            for i in xrange(times):
                model.iterate(G)

            gc = networkx.connected_components(G)[0]
            gc_total += len(gc) / float(n)

        outstring += '{0}\t{1}\n'.format(k, gc_total / float(stats_size))
        k += k_step

    filename = 'opgc_{0}_{1}.dat'.format(n, D)
    outfile = open(filename, 'w')
    outfile.write(outstring)
