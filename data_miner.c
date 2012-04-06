#include <stdio.h>
#include <igraph/igraph.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

#include "model.h"

void main()
{
    unsigned int seed = (unsigned int)time(NULL);
    srand(seed);

    igraph_t *graph;
    igraph_erdos_renyi_game(graph, IGRAPH_ERDOS_RENYI_GNM, 10, 20,
                             IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);

    iterate_many(graph, .5, pow(10,5));    

    igraph_write_graph_edgelist(graph, stdout);
    igraph_destroy(graph);
}
