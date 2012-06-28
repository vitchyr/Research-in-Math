import model
import networkx
import numpy

def write_deg(G, dist_step):
    dist_data = []
    deg_data = []

    for v, deg in G.degree_iter():
        dist = model.dn(G.node[v]['op'], [.5]*G.D)
        dist_data.append(dist)
        deg_data.append(deg)

    bins = []
    dist = 0.0

    while dist < .5 * G.D + .001:
        bins.append(dist)
        dist += dist_step

    bins_np = numpy.array(bins)
    bin_indices = numpy.digitize(dist_data, bins_np)
    histogram = numpy.histogram(dist_data, bins_np)[0]

    mean_degree_data = [0.0] * (len(bins) - 1)
    for i in range(0, len(dist_data) - 1):
        mean_degree_data[bin_indices[i] - 1] += float(deg_data[i]) /\
            histogram[bin_indices[i] - 1] 

    outstring = ''
    for i in range(0, len(bins) - 1):
        outstring += '{0}\t{1}\n'.format(bins[i], mean_degree_data[i])

    k = 2 * G.number_of_edges() / G.number_of_nodes()
    outfile = open('opdegdist_{0}_{1}.dat'.format(k, G.D), 'w')
    outfile.write(outstring)
    outfile.close()

def f(x1):
    return (1 - 2 * x1)**2 / ((x1 - 1) * x1) 

def degC(G):
    total = 0.0

    for x in G.nodes_iter():
        x1 = G.node[x]['op'][0]
        total += f(x1)

    d_mean = (2.0 * G.number_of_edges()) / G.number_of_nodes() 

    return d_mean - G.k * total

def degx(G, x1):
    return G.degC + G.number_of_nodes() * G.k * f(x1)

if __name__ == '__main__':
    n = 2000 
    d_mean = 4.0
    D = 1

    G = model.make_graph(n, 0, D)
    model.construct(G, d_mean)
    print 'm={}'.format(G.number_of_edges())
    #print G.k

    G.degC = degC(G)
    #print G.degC

    #print [degx(G, x1) for x1 in [.1, .2, .3, .4, .5]]
    #print [f(x1) for x1 in [0.01, .1, .2, .3, .49]]
    write_deg(G, .1)
