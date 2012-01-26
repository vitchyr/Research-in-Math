import random
import copy
import math

import networkx
import matplotlib.pyplot

##Model Options
##1. Pick v_0 random & Break with probability
##2. Pick v_0 randomly & Rewire with probability
##3. Pick v_0 via e_0 & Break with probability
##4. Pick v_0 via e_0 & Rewire with probability

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

def absolute_choice(weights):
    return min(weights, key=weights.get)

#Unnormalized breaking probability
def break_pr_function(I, d_neighbor, d_node):
    pr = float(I) / d_neighbor + float(1 - I) / d_node
    return pr

def rewire_pr_function(I, d_someNode, avg_deg):
    pr = I * d_someNode + (1-I) * avg_deg
    return pr

def breakWeighted(graph, I, node):
    weights = {}
    for neighbor in graph.neighbors(node):    
        weights[neighbor] = break_pr_function(I, graph.degree(neighbor), 
            graph.degree(node))   

    node_to_defriend = weighted_choice(weights)
    graph.remove_edge(node, node_to_defriend)

def rewireRandomly(graph, node):
    other_nodes = copy.copy(graph.nodes())
    other_nodes.remove(node)
    while True:
        new_node = random.choice(other_nodes)
        if graph.has_edge(new_node, node):
            other_nodes.remove(new_node)
        else:
            graph.add_edge(node, new_node)
            break

def rewireWeighted(graph, node, I):
    graph_copy = copy.copy(graph.nodes()) #shallow copy of all potential nodes to make a new edge with
    graph_copy.remove(node)
    
    for potentialNode in graph_copy: #remove nodes that already have an edge with *node*
        if graph.has_edge(node, potentialNode):
            graph_copy.remove(potentialNode)
            
    #Probability Setup
    weights = {}
    avg_deg = len(graph.edges())/float(len(graph.nodes()))
    
    for someNode in graph_copy:    
        weights[someNode] = rewire_pr_function(I, graph.degree(someNode), 
            avg_deg)
    #Choose new node to connect to
    new_node = weighted_choice(weights)      
    graph.add_edge(node, new_node)

def iterate(graph, I, m): #m is the model number used (1-4)
    if m<3:
        node = random.choice(graph.nodes())
    else:
        node = random.choice(random.choice(graph.edges()))

    #Checks:
    if graph.degree(node) == 0:
        return
    if len(graph.neighbors(node)) == 0: #double check (didn't work without sometimes)
        return

    #Rewire
    if m%2: #break weighted rewire randomly
        breakWeighted(graph, I, node)
        rewireRandomly(graph, node)
        
    else: #break evenly rewired weighted
        graph.remove_edge(node, random.choice(graph.neighbors(node))) #breaks randomly
        rewireWeighted(graph, node, I)


##if __name__ == '__main__':
##    #Set this stuff manually
##    try:
##        n_nodes = input("How many nodes? ")
##        n_edges = input("Make an edge withedges? ")
##        I = float(input("What I value? "))
##    graph = networkx.erdos_renyi_graph(40, .025)
##    times = 100
##    I = 1
##
##    for i in range(times):
##        iterate(graph, I)
##
##    networkx.draw(graph)
##    matplotlib.pyplot.show()
