#include <igraph/igraph.h>

void main()
{
     igraph_real_t diameter;
     igraph_t graph;
     igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNM, 1000, 4000,
                             IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);
     igraph_diameter(&graph, &diameter, 0, 0, 0, IGRAPH_UNDIRECTED, 1);
     printf("Diameter of a random graph with average degree 5: %f\n",
             (double) diameter);
     igraph_destroy(&graph);

}
