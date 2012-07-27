import model
import pickle

if __name__ == '__main__':
    n = 2000
    k_mean = 4
    times = 1*10**7

    D = 3
    alpha = 2

    G = model.make_opinion_graph(n, .5 * n* k_mean, D, alpha)

    for i in range(times):
        model.iterate(G)

        if i % 10**4 == 0:
            md = model.mean_distance(G)
            print md

    distances = []
    for e in G.edges_iter():
        distances.append(model.distance(G, *e))

    outfile = open('distance_{}_{}.dat'.format(D, alpha), 'w')
    pickle.dump(distances, outfile)
