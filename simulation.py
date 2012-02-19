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

def rewire_weighted(graph, node, I):
    nodes_copy = copy.copy(graph.nodes()) 
    nodes_copy.remove(node)
   
    #Remove nodes already adjacent to v0 
    for potential_node in nodes_copy: 
        if graph.has_edge(node, potential_node):
            nodes_copy.remove(potential_node)
            
    weights = {}
    
    for some_node in nodes_copy:    
        weights[some_node] = rewire_pr_function(I, graph.degree(some_node), 
            graph.avg_degree)

    #Select new node
    new_node = weighted_choice(weights)      
    graph.add_edge(node, new_node)

    return weights[new_node]

def iterate(graph, I, model_no):
    #avg_degree is actually constant - just make sure it's set
    graph.avg_degree = get_avg_degree(graph)

    while True:
        node = random.choice(graph.nodes())

        if graph.degree(node) > 1:
            break

    #break-function model
    if model_no == 1: 
        break_weighted(graph, I, node)
        rewire_randomly(graph, node)
        
    #rewire-function model
    else: 
        old_node = random.choice(graph.neighbors(node)) 
        graph.remove_edge(node, old_node) 

        #this stuff for markov.py
        R_new_node = rewire_weighted(graph, node, I)
        R_old_node = rewire_pr_function(I, graph.degree(old_node), 
            get_avg_degree(graph))

        if R_old_node != 0:
            return R_new_node / R_old_node


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
