import simulation

import networkx
import sys
import random

from numpy import array
from scipy.stats.stats import chisquare

def get_c_rewire(G, v0, I):
    total = 0.0

    for v in simulation.get_Vout(G, v0):
        total += simulation.rewire_pr_function(I, G.degree(v), 
            simulation.get_avg_degree(G))

    return 1.0 / total

def get_exp_flux_rewire(G, v0, v_H, I, restricted):
    V1 = simulation.get_V1(G)

    c = get_c_rewire(G, v0, I)
    R = simulation.rewire_pr_function(I, G.degree(v_H), 
        simulation.get_avg_degree(G))

    if restricted:
        return c * R / G.degree(v0)
    else:
        return c * R / (len(V1) * G.degree(v0))

def get_c_break(G, v0, I):
    total = 0.0

    for v in G.neighbors(v0):
        total += simulation.break_pr_function(I, G.degree(v),
            simulation.get_avg_degree(G))

    return 1.0 / total

def get_exp_flux_break(G, v0, v_G, I, restricted):
    V1 = simulation.get_V1(G)
    Vout = simulation.get_Vout(G, v0)

    c = get_c_break(G, v0, I)
    B = simulation.break_pr_function(I, G.degree(v_G),
        simulation.get_avg_degree(G))

    if restricted:
        return c * B / len(Vout)
    else:
        return c * B / (len(Vout) * len(V1))

def get_obs_freq(from_graph, to_set, I, times, model_no):
    hits = 0

    for i in range(times):
        simulation.print_progress(i, times)

        temp_graph = from_graph.copy()
        simulation.iterate(temp_graph, I, model_no)
        
        if(frozenset(temp_graph.edges()) == to_set):
            hits += 1

    return (times - hits, hits)

def main():
    n_nodes = 10
    n_edges = 12
    I = .6
    times = 10**4 
    model_no = 'R'
    restricted = True

    
    while True:
        G = networkx.gnm_random_graph(n_nodes, n_edges)

        if restricted:
            G.restricted_vP = random.choice(simulation.get_V1(G))

        set_G = set(G.edges())
    
        H = G.copy()
        simulation.iterate(H, I, model_no)
        set_H = set(H.edges())

        #??        
        if set_G != set_H:
            break

    edge_G = set(set_G.difference(H.edges()).pop())
    edge_H = set(set_H.difference(G.edges()).pop())

    v_G = edge_G.difference(edge_H).pop()
    v_H = edge_H.difference(edge_G).pop()
    v0 = edge_G.intersection(edge_H).pop()

    obs_freq = get_obs_freq(G, set_H, I, times, model_no)

    if model_no == 'B':
        exp_flux = get_exp_flux_break(G, v0, v_G, I, restricted)
    elif model_no =='R':
        exp_flux = get_exp_flux_rewire(G, v0, v_H, I, restricted)

    print('')
    print('G = {0}\n'.format(set_G))
    print('H = {0}\n'.format(set_H))

    print('Observed freq = {0}'.format(obs_freq[1]))
    print('Expected freq = {0}'.format(times * exp_flux))

    diff = simulation.rel_diff(obs_freq[1], float(times*exp_flux))
    print('diff = {:.2%}'.format(diff))

if __name__ == '__main__':
    main()

