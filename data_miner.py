import simulation
import matplotlib
import networkx


##This plots average ____ vs. I
##Note: n_something = number of something
##
##Model Options
##1. Pick v_0 random & Break with probability
##2. Pick v_0 randomly & Rewire with probability
##3. Pick v_0 via e_0 & Break with probability
##4. Pick v_0 via e_0 & Rewire with probability
##To change which model you use, change simulation# that is imported
##and used in the nested for-loop ("for j in range(n_iterations):") ~line 50
##You will also want to edit the output file name.

class IterEntry:
    def __str__(self):
        return '%s\t%s\t%s\t%s' % (self.step, self.gc_n_node, self.gc_diameter,
                                   self.n_components)

class Entry:
    def __str__(self):
        return '%s\t%s\t%s\t%s' % (self.I, self.gc_n_nodes, self.gc_diameter,
            self.n_components)


if __name__ == '__main__':
##    n_nodes = 40
##    n_edges = 20
##
##    n_simulations = 200
##    n_steps = 50
##    n_iterations = 100

    try:
        n_nodes = input("How many nodes? ")
        n_edges = input("How many edges? ")
##        I = float(input("What initial I value? "))
        I = 0.0
        n_steps = input("Use how many different I values? ")
        n_simulations = input("Average how many simulations per I value? ")
        n_iterations = input("Use how many iterations per I simulations? ")
        model = input("Model Options:\n\
    1: Pick v_0 random & Break with probability\n\
    2: Pick v_0 randomly & Rewire with probability\n\
    3: Pick v_0 via e_0 & Break with probability\n\
    4: Pick v_0 via e_0 & Rewire with probability\n\
What model do you want to use? ")
    except ValueError:
        print "Please enter integers.\n"

    I_step = 1.0 / float(n_simulations)

    output1 = 'I\tgc_n_nodes\tgc_diameter\tn_components\n'
    output2 = 'Step\tgc_n_nodes\tgc_diameter\tn_components\n'
    
    for i in range(n_steps):

        gc_n_nodes_list = []
        gc_diameter_list = []
        n_components_list = []
        for j in range(n_simulations):
            graph = networkx.gnm_random_graph(n_nodes, n_edges)
            for j in range(n_iterations):
                simulation.iterate(graph, I, model)
            components = networkx.connected_component_subgraphs(graph)
            gc_n_nodes_list.append(components[0].number_of_nodes())
            gc_diameter_list.append(networkx.diameter(components[0]))
            n_components_list.append(len(components))

        components = networkx.connected_component_subgraphs(graph)

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
        simulation.iterate(G, I, model)
        components = networkx.connected_component_subgraphs(G)
        iterBuf = IterEntry()
        iterBuf.step = k
        iterBuf.gc_n_node = components[0].number_of_nodes()
        iterBuf.gc_diameter = networkx.diameter(components[0])
        iterBuf.n_components = len(components)
        output2 += '%s\n' % iterBuf
        
    outfile1 = open('avgResults_gnm_%dm_%dn_%de.dat' % (model, n_nodes, n_edges), 'w')
    outfile1.write(output1)
    outfile1.close()
    outfile2 = open('iterResults_gnm_%dm_%dn_%de.dat' % (model, n_nodes, n_edges), 'w')
    outfile2.write(output2)
    outfile2.close()
