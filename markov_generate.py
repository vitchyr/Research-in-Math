import networkx

import simulation
import sys

if __name__ == '__main__':
    I = 0
    n_nodes = 50
    n_edges = 20
    times = 1000

    counters = {}

    graph = networkx.gnm_random_graph(n_nodes, n_edges) 
    graph.avg_degree = simulation.get_avg_degree(graph)
    edge_set = None

    for i in range(times):
        if i % (times/10) == 0:
            print(str(i/float(times) * 100) + '%')

        #networkx orients the edges automatically
        edge_set = frozenset(graph.edges())

        if edge_set in counters:
            counters[edge_set] += 1
        else:
            counters[edge_set] = 1

        #2 = Rewire-function model
        simulation.iterate(graph, I, 2)
       
    outstring = ''

    for edge_set in counters:
        obs_pi = counters[edge_set]/float(times)
        outstring += '%s\t%d\n' % (edge_set, obs_pi)

    outfile = open('results_markov_%d_%d.dat' % (n_nodes, n_edges), 'w')
    outfile.write(outstring)
