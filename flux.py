import simulation

import networkx
import sys

from numpy import array
from scipy.stats.stats import chisquare

def get_c_rewire(G, v0, I):
    total = 0.0

    for v in simulation.get_Vout(G, v0):
        total += simulation.rewire_pr_function(I, G.degree(v), 
            simulation.get_avg_degree(G))

    return 1.0 / total

def get_exp_flux_rewire(G, v0, v_H, I):
    V1 = simulation.get_V1(G)

    c = get_c_rewire(G, v0, I)
    R = simulation.rewire_pr_function(I, G.degree(v_H), 
        simulation.get_avg_degree(G))

    return c * R / (len(V1) * G.degree(v0))

def get_c_break(G, v0, I):
    total = 0.0

    for v in G.neighbors(v0):
        total += simulation.break_pr_function(I, G.degree(v),
            simulation.get_avg_degree(G))

    return 1.0 / total

def get_exp_flux_break(G, v0, v_G, I):
    V1 = simulation.get_V1(G)
    Vout = simulation.get_Vout(G, v0)

    c = get_c_break(G, v0, I)
    B = simulation.break_pr_function(I, G.degree(v_G),
        simulation.get_avg_degree(G))

    return c * B / (len(V1) * len(Vout))

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
    n_nodes = 4
    n_edges = 2
    I = .99
    times = 10**5 
    model_no = 'R'
    
    while True:
        #G = networkx.gnm_random_graph(n_nodes, n_edges)
        G = networkx.Graph()
        G.add_edge(1, 2)
        G.add_edge(0, 3)

        set_G = set(G.edges())
    
        H = networkx.Graph()
        H.add_edge(1, 2)
        H.add_edge(3, 2)
        H.add_node(0)

        #H = G.copy()
        #simulation.iterate(H, I, model_no)
        set_H = set(H.edges())
        
        if set_G != set_H:
            break

    edge_G = set(set_G.difference(H.edges()).pop())
    edge_H = set(set_H.difference(G.edges()).pop())

    v_G = edge_G.difference(edge_H).pop()
    v_H = edge_H.difference(edge_G).pop()
    v0 = edge_G.intersection(edge_H).pop()

    obs_freq = get_obs_freq(G, set_H, I, times, model_no)

    if model_no == 'B':
        exp_flux = get_exp_flux_break(G, v0, v_G, I)
    elif model_no =='R':
        exp_flux = get_exp_flux_rewire(G, v0, v_H, I)

    obs_freq_np = array(obs_freq)
    exp_freq_np = array((times * (1.0 - exp_flux), times * exp_flux))

    print('')
    print('G = {0}\n'.format(set_G))
    print('H = {0}\n'.format(set_H))

    print('Observed freq = {0}'.format(obs_freq[1]))
    print('Expected freq = {0}'.format(times * exp_flux))

    p_value = chisquare(obs_freq_np, exp_freq_np)[1]
    print('p_value = {:.2%}'.format(float(p_value)))

if __name__ == '__main__':
    main()

