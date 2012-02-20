import simulation

import networkx
import sys

def get_c(G, v0, I):
    total = 0.0

    for v in simulation.get_Vout(G, v0):
        total += simulation.rewire_pr_function(I, G.degree(v), 
            simulation.get_avg_degree(G))

    return 1.0 / total

def get_exp_flux(G, v0, v_H, I):
    V1 = simulation.get_V1(G)
    c = get_c(G, v0, I)
    R = simulation.rewire_pr_function(I, G.degree(v_H), 
        simulation.get_avg_degree(G))

    return c * R / (len(V1) * G.degree(v0))

def get_obs_flux(from_graph, to_set, I, times):
    hits = 0

    for i in range(times):
        simulation.print_progress(i, times)

        temp_graph = from_graph.copy()
        simulation.iterate(temp_graph, I, 2)
        
        if(frozenset(temp_graph.edges()) == to_set):
            hits += 1

    return float(hits) / times

def main():
    n_nodes = 5
    n_edges = 3
    I = 0.5
    times = 100000
    
    while True:
        G = networkx.gnm_random_graph(n_nodes, n_edges)
        set_G = set(G.edges())
    
        #Rewire-function
        H = G.copy()
        simulation.iterate(H, I, 2)
        set_H = set(H.edges())
        
        if set_G != set_H:
            break

    edge_G = set(set_G.difference(H.edges()).pop())
    edge_H = set(set_H.difference(G.edges()).pop())

    v_G = edge_G.difference(edge_H).pop()
    v_H = edge_H.difference(edge_G).pop()
    v0 = edge_G.intersection(edge_H).pop()

    obs_flux = get_obs_flux(G, set_H, I, times)
    exp_flux = get_exp_flux(G, v0, v_H, I)

    print('')
    print('G = {0}\n'.format(set_G))
    print('H = {0}\n'.format(set_H))

    print('Observed flux = {0}'.format(obs_flux))
    print('Expected flux = {0}'.format(exp_flux))

    diff = simulation.abs_diff(obs_flux, exp_flux)
    print('Difference = {:.2%}'.format(diff))

if __name__ == '__main__':
    main()

