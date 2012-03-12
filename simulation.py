import random
import copy
import sys

import networkx
import matplotlib

def print_progress(i, times):
    if i % (times / 10) == 0 and i != 0:
        print('{:.0%} done'.format(float(i)/times))

def get_degree_distro(graph):
    distro = [0] * (graph.number_of_nodes() - 1)

    for v, deg in graph.degree_iter():
        distro[deg] += 1 

    return distro

#absolute-valued relative difference
def rel_diff(n1, n2):
    return abs(n1 - n2) / (float(n1 + n2) / 2)

def get_V1(graph):
    V1 = [] 

    for v, degree in graph.degree_iter():
        if degree > 0 and degree < graph.number_of_nodes() - 1:
            V1.append(v)

    return V1 

def weighted_choice(weights):
    totals = {}
    running_total = 0

    for key in weights:
        running_total += weights[key]
        totals[key] = running_total

    rnd = random.random() * running_total

    for key in totals:
        if rnd < totals[key]:
            return key

def break_pr_function(I, deg_v, avg_degree):
    return float(I) / deg_v + (1.0 - I) / avg_degree

def rewire_pr_function(I, deg_v, avg_degree):
    return I * deg_v + (1.0 - I) * avg_degree

def get_avg_degree(graph):
    return 2 * graph.number_of_edges() / float(graph.number_of_nodes()) 

def break_weighted_select(graph, v0, I):
    weights = {}

    for v in graph.neighbors(v0):
        weights[v] = break_pr_function(I, graph.degree(v),
            get_avg_degree(graph))   

    return weighted_choice(weights)

def rewire_randomly_select(graph, v0):
    Vout = get_Vout(graph, v0)
    return random.choice(Vout)

def get_Vout(graph, v0):
    Vout = []

    for v in graph.nodes_iter():
        if not graph.has_edge(v0, v) and v != v0:
            Vout.append(v)

    return Vout

def rewire_weighted_select(graph, v0, I):
    weights = {}
   
    #BIG CHANGE: Don't let v0 rewire to the node it just broke with 
    #Hopefully this doesn't screw up our other curves
    for v in get_Vout(graph, v0):
        weights[v] = rewire_pr_function(I, graph.degree(v),
            get_avg_degree(graph))

    #Return selected node
    return weighted_choice(weights)      


def iterate(graph, I, model_no):
    if 'restricted_vP' in graph.__dict__:
        v0 = graph.restricted_vP
    else:
        while True:
            v0 = random.choice(graph.nodes())

            if(graph.degree(v0) > 0 and
                graph.degree(v0) < graph.number_of_nodes() - 1):
                break

    #break-function model
    if model_no[0] == 'B': 
        old_node = break_weighted_select(graph, v0, I)
        new_node = rewire_randomly_select(graph, v0)
        
    #rewire-function model
    elif model_no[0] == 'R': 
        old_node = random.choice(graph.neighbors(v0)) 
        new_node = rewire_weighted_select(graph, v0, I)

    else:
        raise ValueError("Unsupported model!")

    graph.remove_edge(v0, old_node) 
    graph.add_edge(v0, new_node)

if __name__ == '__main__':
    write_deg_distro = True
    display_graph = False

    try:
        n_nodes = input("How many nodes? ")
        n_edges = input("How many edges? ")
        I = float(input("What I value? "))
        model_no = raw_input("Model number? (R/B) ")
        times = input("How many iterations? ")
    except:
        print("Invalid input. Exiting...")
        sys.exit(1)

    graph = networkx.gnm_random_graph(n_nodes, n_edges)

    for i in range(times):
        iterate(graph, I, model_no)

    if display_graph:
        networkx.draw(graph)
        matplotlib.pyplot.show()

    if write_deg_distro:
        distro = get_degree_distro(graph)
        outstring = ''

        for i in range(len(distro)):
            outstring += '{0}\t{1}\n'.format(i, distro[i])

        filename = 'degree_distro_{0}_{1}_{2}.dat'.format(model_no,
            n_nodes, n_edges)
        outfile = open(filename, 'w')
        outfile.write(outstring)
