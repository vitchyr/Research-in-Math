import random
import copy
import sys

import networkx
import matplotlib

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

def break_pr_function(I, d_neighbor, avg_degree):
    return float(I) / d_neighbor + float(1 - I) / avg_degree

def rewire_pr_function(I, d_someNode, avg_degree):
    return I * d_someNode + (1-I) * avg_degree

def get_avg_degree(graph):
    return 2 * graph.number_of_edges() / float(graph.number_of_nodes()) 

def break_weighted(graph, I, node):
    weights = {}

    for neighbor in graph.neighbors(node):    
        weights[neighbor] = break_pr_function(I, graph.degree(neighbor), 
            graph.avg_degree)   

    node_to_defriend = weighted_choice(weights)
    graph.remove_edge(node, node_to_defriend)

def rewire_randomly(graph, node):
    other_nodes = copy.copy(graph.nodes())
    other_nodes.remove(node)
    while True:
        new_node = random.choice(other_nodes)
        if graph.has_edge(new_node, node):
            other_nodes.remove(new_node)
        else:
            graph.add_edge(node, new_node)
            break

def get_Vout(graph, v0):
    Vout = []

    for node in graph.nodes_iter():
        if not graph.has_edge(v0, node) and node != v0:
            Vout.append(node)

    return Vout

def rewire_weighted_select(graph, node, I):
    weights = {}
   
    #BIG CHANGE: Don't let v0 rewire to the node it just broke with 
    #Hopefully this doesn't screw up our other curves
    for some_node in get_Vout(graph, node):
        weights[some_node] = rewire_pr_function(I, graph.degree(some_node), 
            graph.avg_degree)

    #Return selected node
    return weighted_choice(weights)      


def iterate(graph, I, model_no):
    #avg_degree is actually constant, but can get messed up when graph
    #is in an intermediate state
    graph.avg_degree = get_avg_degree(graph)

    while True:
        node = random.choice(graph.nodes())

        if graph.degree(node) > 0:
            break

    #break-function model
    if model_no == 1: 
        break_weighted(graph, I, node)
        rewire_randomly(graph, node)
        
    #rewire-function model
    else: 
        old_node = random.choice(graph.neighbors(node)) 
        new_node = rewire_weighted_select(graph, node, I)

        graph.remove_edge(node, old_node) 
        graph.add_edge(node, new_node)

if __name__ == '__main__':
    try:
        n_nodes = input("How many nodes? ")
        n_edges = input("How many edges? ")
        I = float(input("What I value? "))
        model_no = input("Model number? (1/2) ")
        times = input("How many iterations? ")
    except:
        print("Invalid input. Exiting...")
        sys.exit(1)

    graph = networkx.gnm_random_graph(n_nodes, n_edges)

    for i in range(times):
        iterate(graph, I, model_no)

    networkx.draw(graph)
    matplotlib.pyplot.show()
