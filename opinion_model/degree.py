import model

def write_deg(G, dist_step):
    dist_data = []
    deg_data = []

    for v, deg in G.degree_iter():
        dist = dn(G.node[v]['op'], [.5]*G.D)
        dist_data.append(dist)
        deg_data.append(deg)

    import numpy
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

if __name__ == '__main__':
