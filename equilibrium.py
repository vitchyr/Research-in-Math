import networkx
import simulation
import random

from numpy import array
from scipy.stats.stats import chisquare
from collections import OrderedDict

def get_unnormalized_pi_break_restricted(graph, I):
    vP = graph.restricted_vP

    product = 1.0
    c_denom = 0.0

    for v in graph.neighbors(vP):
        B = simulation.break_pr_function(I, graph.degree(v), 
            simulation.get_avg_degree(graph))

        c_denom += B
        product *= 1.0 / B

    c = 1.0 / c_denom

    V1 = simulation.get_V1(graph)
    Vout = simulation.get_Vout(graph, vP)
    K_restricted = c / len(Vout)

    return product / K_restricted 

def get_unnormalized_pi_break(graph, I):
    V1 = simulation.get_V1(graph)

    unnormalized_pi = 0.0

    for v0 in V1:
        product = 1.0
        c_denom = 0.0

        for v in graph.neighbors(v0):
            B = simulation.break_pr_function(I, graph.degree(v), 
                simulation.get_avg_degree(graph))

            c_denom += B
            product *= 1.0 / B

        c = 1.0 / c_denom

        Vout = simulation.get_Vout(graph, v0)
        unnormalized_pi += product * (len(V1) * len(Vout)) / c

    return unnormalized_pi / len(V1)

def get_delta_nodes(graph):
    delta_nodes = {}

    for v0 in simulation.get_V1(graph):
        delta_nodes[v0] = graph.degree(v0) *\
            len(simulation.get_Vout(graph, v0)) 

    return delta_nodes

def get_unnormalized_pi_rewire_restricted(graph, I):
    vP = graph.restricted_vP

    Vout = simulation.get_Vout(graph, vP)
    product = 1.0
    c_denom = 0.0

    for v in Vout:
        R = simulation.rewire_pr_function(I, graph.degree(v), 
            simulation.get_avg_degree(graph))

        c_denom += R
        product *= 1.0 / R

    c = 1.0 / c_denom
    K_restricted = c / (graph.degree(vP))         

    return product / K_restricted

def get_unnormalized_pi_rewire(graph, I):
    V1 = simulation.get_V1(graph)
    delta_nodes = get_delta_nodes(graph)
    delta_graph = sum(delta_nodes.values())

    unnormalized_pi = 0.0

    for v0 in V1:
        Vout = simulation.get_Vout(graph, v0)
        product = 1.0
        c_denom = 0.0

        for v in Vout:
            R = simulation.rewire_pr_function(I, graph.degree(v), 
                simulation.get_avg_degree(graph))

            c_denom += R
            product *= 1.0 / R

        c = 1.0 / c_denom
        K_R = c / (graph.degree(v0))         
        delta_ratio = float(delta_nodes[v0]) / delta_graph
        unnormalized_pi += delta_ratio * product / K_R

    return unnormalized_pi

if __name__ == '__main__':
    I = .99
    n_nodes = 4
    n_edges = 2
    times = 10**6
    model_no = 'R'
    restricted = False
    verbose = True

    obs_freq = OrderedDict()
    unnormalized_pi = {}

    graph = networkx.gnm_random_graph(n_nodes, n_edges) 

    if restricted:
        graph.restricted_vP = random.choice(simulation.get_V1(graph))

    for i in xrange(times):
        simulation.print_progress(i, times)

        simulation.iterate(graph, I, model_no)

        #networkx orients the edges automatically
        edge_set = frozenset(graph.edges())

        if edge_set in obs_freq:
            obs_freq[edge_set] += 1
        else:
            obs_freq[edge_set] = 1

        if edge_set not in unnormalized_pi:

            if model_no == 'B':

                if restricted:
                    unnormalized_pi[edge_set] =\
                        get_unnormalized_pi_break_restricted(graph, I)
                else:
                    unnormalized_pi[edge_set] =\
                        get_unnormalized_pi_break(graph, I)

            elif model_no == 'R':

                if restricted:
                    unnormalized_pi[edge_set] =\
                        get_unnormalized_pi_rewire_restricted(graph, I)
                else:
                    unnormalized_pi[edge_set] =\
                        get_unnormalized_pi_rewire(graph, I)
       
    unnormalized_pi_sum = sum(unnormalized_pi.values())
    exp_freq = []

    for edge_set in obs_freq:
        exp_pi = unnormalized_pi[edge_set]/unnormalized_pi_sum
        exp_freq.append(exp_pi * times)

        print(obs_freq[edge_set], exp_freq[-1:][0])

        #diff = simulation.rel_diff(obs_pi[edge_set], exp_pi[edge_set])

        #if verbose:
        #    print(edge_set, obs_pi[edge_set], exp_pi[edge_set], diff)

        #diffs.append(diff)

    exp_freq_np = array(exp_freq)
    obs_freq_np = array(obs_freq.values())

    p_value = chisquare(obs_freq_np, exp_freq_np)[1]

    #mean_diff = sum(diffs) / float(len(diffs))

    print('')
    print('p_value = {:.2%}'.format(float(p_value)))
    #print('Mean difference = {:.2%}'.format(mean_diff))
