import networkx

import simulation

I = .5
n_nodes = 10
n_edges = 4
times = 1000

    
if __name__ == '__main__':
    counters = {}

    #Unnormalized equilibrium probabilities
    tau = {}

    graph = networkx.gnm_random_graph(n_nodes, n_edges) 
    tau[frozenset(graph.edges())] = 1.0

    for i in xrange(times):
        #networkx orients the edges automatically
        edge_set = frozenset(graph.edges())

        if edge_set in counters:
            counters[edge_set] += 1
        else:
            counters[edge_set] = 1

        if edge_set not in tau:
            print old_tau_val
            tau[edge_set] = old_tau_val * tau_ratio

        old_tau_val = tau[edge_set]

        #Rewire-function model
        tau_ratio = simulation.iterate(graph, I, 2)
       
    assert sum(counters.values()) == times
    tau_sum = sum(tau.values())

    obs_pi = {}
    exp_pi = {}
    diffs = []

    for edge_set in counters:
        obs_pi[edge_set] = counters[edge_set]/float(times)
        exp_pi[edge_set] = tau[edge_set]/tau_sum

        print((obs_pi[edge_set], exp_pi[edge_set]))

        dev = (obs_pi[edge_set] - exp_pi[edge_set])
        avg = (obs_pi[edge_set] + exp_pi[edge_set]) / 2

        diffs.append(dev/avg)

    print '\n\n'
    print(sum(diffs)/float(len(diffs)))
