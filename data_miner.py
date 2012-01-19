import simulation

import corestats
import matplotlib
import networkx

class Entry:

    def __str__(self):
        return '%s|%s|%s|%s' % (self.I, self.gc_n_nodes, self.gc_diameter,
            self.n_components)


if __name__ == '__main__':
    n_nodes = 10
    n_edges = 5

    n_simulations = 5
    n_iterations = 1000

    graph = networkx.gnm_random_graph(n_nodes, n_edges)

    I = 0.0
    I_step = 1.0 / float(n_simulations)

    entries = []

    for i in range(n_simulations):

        for j in range(n_iterations):
            simulation.iterate(graph, I)

        components = networkx.connected_component_subgraphs(graph)

        entry = Entry()
        entry.I = I

        entry.gc_n_nodes = components[0].number_of_nodes()
        entry.gc_diameter = networkx.diameter(components[0])
        entry.n_components = len(components)

        entries.append(entry)
        I += I_step

        print entry
        networkx.draw(graph)
        matplotlib.pyplot.show()

    output = 'I|gc_n_nodes|gc_diameter|n_components'

    for entry in entries:
        output += '\n%s' % entry
    
    outfile = open('results_gnm_%d_%d.dat' % (n_nodes, n_edges), 'w')
    outfile.write(output)
