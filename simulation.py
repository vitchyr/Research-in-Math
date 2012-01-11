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

def pr_function(I, c, ds, d0):
    return I * c / ds + (1.0 - I) / d0

def iterate(graph):
    node = random.choice(graph.nodes())    
    
    if graph.degree(node) == 0:
        return

    #Uninitialized
    deg_min = -1
    
    for neighbor in graph.neighbors(node):    
        if(deg_min == -1 or graph.degree(neighbor) < deg_min):
            deg_min = graph.degree(neighbor)

    weights = {}

    for neighbor in graph.neighbors(node):    
        weights[neighbor] = pr_function(I, deg_min, graph.degree(neighbor), 
            graph.degree(node))   

    node_to_defriend = weighted_choice(weights)
    graph.remove_edge(node, node_to_defriend)

    other_nodes = copy.copy(graph.nodes())
    other_nodes.remove(node)
    new_node = random.choice(other_nodes)

    graph.add_edge(node, new_node)
        

if __name__ == '__main__':
    
    #Set this stuff manually
    graph = networkx.erdos_renyi_graph(10, .15)
    times = 100
    I = 0

    for i in range(times):
        iterate(graph)

    networkx.draw(graph)
    matplotlib.pyplot.show()
