import random
import copy

import networkx
import matplotlib.pyplot

def weighted_choice(weights):
    totals = {}
    running_total = 0

    for key, weight in weights.iteritems():
        running_total += weight
        totals[key] = running_total

    rnd = random.random() * running_total
    for key, total in totals.iteritems():
        if rnd < total:
            return key

def add_random_edge(graph):
    while True:
        node1 = random.choice(graph.nodes())
        node2 = random.choice(graph.nodes())

        if(node1 != node2 and not graph.has_edge(node1, node2)):
            G.add_edge(node1, node2)
            break

def pr_function(I, c, ds, d0):
    return I * c / ds + (1.0 - I) / d0

def iterate(graph):
    node = random.choice(graph.nodes())    
    
    if graph.degree(node) == 0:
        return
    
    inverse_sum = 0.0
    for neighbor in graph.neighbors(node):    
        inverse_sum += 1.0 / float(graph.degree(neighbor))

    c = 1.0 / inverse_sum

    weights = {}

    for neighbor in graph.neighbors(node):    
        weights[neighbor] = pr_function(I, c,  graph.degree(neighbor), 
            graph.degree(node))   


    node_to_defriend = weighted_choice(weights)
    graph.remove_edge(node, node_to_defriend)

    #Rewire
    if graph.degree(node) == len(graph.nodes()) - 1:
        add_random_edge(graph)
    else:
        other_nodes = copy.copy(graph.nodes())
        other_nodes.remove(node)

        while True:
            new_node = random.choice(other_nodes)
            
            if graph.has_edge(new_node, node):
                other_nodes.remove(new_node)
            else:
                graph.add_edge(node, new_node)
                break


if __name__ == '__main__':
    
    #Set this stuff manually
    graph = networkx.erdos_renyi_graph(40, .15)
    times = 10000
    I = 1

    for i in range(times):
        iterate(graph)

    networkx.draw_circular(graph)
    matplotlib.pyplot.show()
