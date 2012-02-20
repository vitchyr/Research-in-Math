import networkx
import simulation

def get_V1(graph):
    V1 = [] 

    for node, degree in graph.degree_iter():
        if degree > 0:
            V1.append(node)

    return V1 


def get_unnormalized_pi(graph, I):
    V1 = get_V1(graph)

    unnormalized_pi = 0.0

    for v0 in V1:
        Vout = get_Vout(graph, v0)
        product = 1.0

        for node in Vout:
            R = simulation.rewire_pr_function(I, graph.degree(node),
                graph.avg_degree)

            product *= 1.0 / R

        unnormalized_pi += product

    return unnormalized_pi

if __name__ == '__main__':
    I = .5
    n_nodes = 30
    n_edges = 20
    times = 10000

    counters = {}

    unnormalized_pi = {}

    graph = networkx.gnm_random_graph(n_nodes, n_edges) 

    for i in xrange(times):
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

        print((obs_pi[edge_set], exp_pi[edge_set]))

        dev = abs(obs_pi[edge_set] - exp_pi[edge_set])
        avg = (obs_pi[edge_set] + exp_pi[edge_set]) / 2

        diffs.append(dev/avg)

    print '\n\n'
    print(sum(diffs)/float(len(diffs)))
