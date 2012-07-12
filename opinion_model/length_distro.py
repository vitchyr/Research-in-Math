import model
import corestats

if __name__ == '__main__':
    n = 500

    G = model.make_opinion_graph(n, 0, 1)
    c=[0.01196013437, .000801687, .000006662]
    model.construct(G, c[2], 'c')
    print G.number_of_edges()

    distances = []
    for e in G.edges_iter():
        distances.append(model.distance(G, *e))

    stats = corestats.Stats(distances)
    print(stats.avg(), stats.stdev()) 
