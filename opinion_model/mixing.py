import model

if __name__ == '__main__':
    n = 200
    k_mean = 4
    D = 1

    times = 10**7
    period = 10**5

    G = model.make_opinion_graph(n, .5 * n * k_mean, D) 
    outstring = ''

    for i in xrange(times):
        model.iterate(G)

        if i % period == 0:
            s = '{0}\t{1}\n'.format(i, model.mean_distance(G))
            outstring += s

            if i % (10*period) == 0:
                print s

    outfile = open('mixing.dat', 'w')
    outfile.write(outstring)
