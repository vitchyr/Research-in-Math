import model
import corestats

if __name__ == '__main__':
    n = 2000
    D = 3
    G = model.make_opinion_graph(n, 0, D, True)

    #for k = 4
    #n = 500
    #c=[0.01196013437, .000801687, .000006662]

    #n = 2000
    #           1D                2D             3D ...]
    c=[3.91006469727e-07, 0.000122680664062, 0.000608520507813, 0.001376953125, 0.002392578125, 0.003642578125]

    #looping, <k> = 4, n=5000, D=[1,2,3]
    #c=[2.23517417908e-08, 1.23977661133e-05, 7.91549682617e-05]
    model.construct(G, c[D-1], 'c')
    print G.number_of_edges()

    distances = []
    for e in G.edges_iter():
        distances.append(model.distance(G, *e))

    outstring = str(distances)
    outstring = outstring[1:-1]
    outfile = open("data/length_Distro_{0}D.dat".format(D), "w")
    outfile.write(outstring)
    outfile.close()
    stats = corestats.Stats(distances)
    print(stats.avg(), stats.stdev()) 
