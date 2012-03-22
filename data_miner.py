import simulation
import networkx

class IterEntry:
    def __str__(self):
        return '%s\t%s\t%s\t%s' % (self.step, self.gc_n_node, self.gc_diameter,
                                   self.n_components)

class Entry:
    def __str__(self):
        return '%s\t%s\t%s\t%s' % (self.I, self.gc_n_nodes, self.gc_diameter,
            self.n_components)


if __name__ == '__main__':

    try:
        n_nodes = input("How many nodes? ")
        n_edges = input("How many edges? ")
        n_steps = input("Use how many different I values? ")
        n_simulations = input("Average how many simulations per I value? ")
        n_iterations = input("Use how many iterations per I simulations? ")
        model_no = raw_input("Model Options:\n\
    B: Break-function model\n\
    R: Rewire-function model\n\
What model do you want to use? ")
    except (ValueError, SyntaxError):
        print "Please enter integers.\n"

    I = 0.0
    I_step = 1.0 / float(n_steps)

    output1 = 'I\tgc_n_nodes\tgc_diameter\tn_components\n'
    output2 = 'Step\tgc_n_nodes\tgc_diameter\tn_components\n'
    
    for i in range(n_steps):

        for j in range(1, 4):
            if j * n_steps / 4 == i:
                print(str(j * 25) + "% done")

        gc_n_nodes_list = []
        gc_diameter_list = []
        n_components_list = []

        for j in range(n_simulations):
            graph = networkx.gnm_random_graph(n_nodes, n_edges)

            for j in range(n_iterations):
                simulation.iterate(graph, I, model_no)

            components = networkx.connected_component_subgraphs(graph)
            gc_n_nodes_list.append(components[0].number_of_nodes())
            gc_diameter_list.append(networkx.diameter(components[0]))
            n_components_list.append(len(components))

        entry = Entry()
        entry.I = I

        entry.gc_n_nodes = float(sum(gc_n_nodes_list))/len(gc_n_nodes_list)
        entry.gc_diameter = float(sum(gc_diameter_list))/len(gc_diameter_list)
        entry.n_components = float(sum(n_components_list))/len(n_components_list)

        output1 += '%s\n' % entry
        I += I_step

    #Comparing iterations
    G = networkx.gnm_random_graph(n_nodes, n_edges)
    for k in range(n_iterations):
        simulation.iterate(G, I, model_no)
        components = networkx.connected_component_subgraphs(G)
   
        iterBuf = IterEntry()
        iterBuf.step = k
        iterBuf.gc_n_node = components[0].number_of_nodes()
        iterBuf.gc_diameter = networkx.diameter(components[0])
        iterBuf.n_components = len(components)
   
        output2 += '%s\n' % iterBuf
       
    filename1 = 'avgResults_gnm_%s_%dn_%de.dat' % (model_no, n_nodes, n_edges) 
    outfile1 = open(filename1, 'w')
    outfile1.write(output1)
    outfile1.close()
    print('Wrote file: {0}'.format(filename1))

    filename2 = 'iterResults_gnm_%s_%dn_%de.dat' % (model_no, n_nodes, n_edges)
    outfile2 = open(filename2, 'w')
    outfile2.write(output2)
    outfile2.close()
    print('Wrote file: {0}'.format(filename2))
