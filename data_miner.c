#include <igraph/igraph.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

#include "model.h"

void main(int argc, char *argv[])
{
    int n_nodes, n_edges, stats_size = 0;
    float th_min, th_step, th_max;

    if(argc > 5)
    {
        n_nodes = atoi(argv[1]);
        n_edges = atoi(argv[2]);
        th_min = atof(argv[3]);
        th_step = atof(argv[4]);
        th_max = atof(argv[5]);

        if(argc > 6)
        {
            stats_size = atoi(argv[6]);
        }
    } else {
        printf("Syntax: ./data_miner n m th_min th_step th_max [stats_size]\n");
        printf("Exiting...\n");
        return;
    }

    unsigned int seed = (unsigned int)time(NULL);
    srand(seed);

    igraph_t graph;
    igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNM, 10, 20,
                             IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);

    iterate_many(&graph, .5, pow(10,5));    

    igraph_write_graph_edgelist(&graph, stdout);
    igraph_destroy(&graph);
}
