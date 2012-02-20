import networkx
import simulation
import flux


def get_unnormalized_pi(graph, I):
    V1 = simulation.get_V1(graph)

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

        unnormalized_pi += product * (len(V1) * graph.degree(v0)) / c

    return unnormalized_pi

if __name__ == '__main__':
    I = 0
    n_nodes = 5
    n_edges = 3
    times = 20000

    counters = {}

    unnormalized_pi = {}

    graph = networkx.gnm_random_graph(n_nodes, n_edges) 

    for i in xrange(times):
        simulation.print_progress(i, times)

        #Rewire-function model
        simulation.iterate(graph, I, 2)

        #networkx orients the edges automatically
        edge_set = frozenset(graph.edges())

        if edge_set in counters:
            counters[edge_set] += 1
        else:
            counters[edge_set] = 1

        if edge_set not in unnormalized_pi:
            unnormalized_pi[edge_set] = get_unnormalized_pi(graph, I) 
       
    obs_pi = {}
    exp_pi = {}
    diffs = []

    unnormalized_pi_sum = sum(unnormalized_pi.values())

    for edge_set in counters:
        obs_pi[edge_set] = counters[edge_set]/float(times)
        exp_pi[edge_set] = unnormalized_pi[edge_set]/unnormalized_pi_sum

        dev = abs(obs_pi[edge_set] - exp_pi[edge_set])
        avg = (obs_pi[edge_set] + exp_pi[edge_set]) / 2

        diffs.append(dev/avg)

    mean_diff = sum(diffs) / float(len(diffs))

    print('')
    print('Mean difference = {:.2%}'.format(mean_diff))
