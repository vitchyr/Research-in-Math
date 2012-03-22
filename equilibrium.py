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

    return product / c 

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

    return product / c 


if __name__ == '__main__':
    I = .6
    n_nodes = 15
    n_edges = 25
    times = 10**4
    model_no = 'R'
    restricted = True
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
                    raise ValueError

            elif model_no == 'R':

                if restricted:
                    unnormalized_pi[edge_set] =\
                        get_unnormalized_pi_rewire_restricted(graph, I)
                else:
                    raise ValueError
       
    unnormalized_pi_sum = sum(unnormalized_pi.values())
    exp_freq = []

    for edge_set in obs_freq:
        exp_pi = unnormalized_pi[edge_set]/unnormalized_pi_sum
        exp_freq.append(exp_pi * times)

        if verbose:
            diff = simulation.rel_diff(obs_freq[edge_set], exp_freq[-1])
            print(obs_freq[edge_set], exp_freq[-1:][0], diff)

    exp_freq_np = array(exp_freq)
    obs_freq_np = array(obs_freq.values())

    p_value = chisquare(obs_freq_np, exp_freq_np)[1]

    print('')
    print('p_value = {:.2%}'.format(float(p_value)))
