import networkx
import simulation
import flux

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
        delta_nodes[v0] = graph.degree(v0) *len(simulation.get_Vout(graph, v0)) 

    return delta_nodes

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
        K_R = c / (len(V1) * graph.degree(v0))         
        delta_ratio = float(delta_nodes[v0]) / delta_graph
        unnormalized_pi += delta_ratio * product / K_R

    return unnormalized_pi

if __name__ == '__main__':
    I = .99
    n_nodes = 4
    n_edges = 2
    times = 10**5
    model_no = 2

    counters = {}

    unnormalized_pi = {}

    graph = networkx.gnm_random_graph(n_nodes, n_edges) 

    for i in xrange(times):
        simulation.print_progress(i, times)

        simulation.iterate(graph, I, model_no)

        #networkx orients the edges automatically
        edge_set = frozenset(graph.edges())

        if edge_set in counters:
            counters[edge_set] += 1
        else:
            counters[edge_set] = 1

        if edge_set not in unnormalized_pi:

            if model_no == 1:
                unnormalized_pi[edge_set] =\
                    get_unnormalized_pi_break(graph, I)
            else:
                unnormalized_pi[edge_set] =\
                    get_unnormalized_pi_rewire(graph, I) 
       
    obs_pi = {}
    exp_pi = {}
    diffs = []

    unnormalized_pi_sum = sum(unnormalized_pi.values())

    for edge_set in counters:
        obs_pi[edge_set] = counters[edge_set]/float(sum(counters.values()))
        exp_pi[edge_set] = unnormalized_pi[edge_set]/unnormalized_pi_sum

        diff = simulation.abs_diff(obs_pi[edge_set], exp_pi[edge_set])
        print(edge_set, obs_pi[edge_set], exp_pi[edge_set], diff)

        diffs.append(diff)

    mean_diff = sum(diffs) / float(len(diffs))

    print('')
    print('Mean difference = {:.2%}'.format(mean_diff))
