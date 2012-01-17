import simulation

import corestats
import networkx

class Entry:

    def __str__(self):
        return '%s|%s|%s|%s' % (self.I, self.gc_n_nodes, self.gc_diameter,
            self.degree_stdev)


if __name__ == '__main__':
    n_nodes = 40
    n_edges = 20

    n_simulations = 1000
    n_iterations = 1000

    graph = networkx.gnm_random_graph(n_nodes, n_edges)

    I = 0.0
    I_step = 1.0 / float(n_simulations)

    entries = []

    for i in range(n_simulations):

        for j in range(n_iterations):
            simulation.iterate(graph, I)

        components = networkx.connected_component_subgraphs(graph)

        max_size = 0
        max_size_id = 0

        for i, component in enumerate(components):
            if component.number_of_nodes() > max_size:
                max_size = component.number_of_nodes()
                max_size_id = i

        entry = Entry()
        entry.I = I

        entry.gc_n_nodes = max_size 
        entry.gc_diameter = networkx.diameter(components[max_size_id])

        degree_list_stats = corestats.Stats(graph.degree().values())
        entry.degree_median = degree_list_stats.median()
        entry.degree_stdev = degree_list_stats.stdev()

        entries.append(entry)
        I += I_step

    output = 'I|gc_n_nodes|gc_diameter|degree_stdev'

    for entry in entries:
        output += '\n%s' % entry
    
    outfile = open('results_gnm_%d_%d.dat' % (n_nodes, n_edges), 'w')
    outfile.write(output)
