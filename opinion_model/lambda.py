import model
import networkx

if __name__ == '__main__':
    n = 5000
    D = 1

    space = .1
    n_data_vertices = 11
    times = 1

    data_vertices = []
    data = [0.0]*n_data_vertices

    for i in xrange(times):
        G = model.make_opinion_graph(n - n_data_vertices, 0, D)

        v = 0.0
        for j in xrange(n_data_vertices):
            G.add_node((v,))
            data_vertices.append((v,))
            v += space

        model.construct(G, 6.5041*10**-8, 'c')

        for j in xrange(n_data_vertices):
            data[j] += G.degree(data_vertices[j]) / float(times)

    outstring = ''
    for i in xrange(n_data_vertices):
        outstring += '{0}\t{1}\n'.format(space * i, data[i])

    outfile = open('lambda.dat', 'w')
    outfile.write(outstring)
