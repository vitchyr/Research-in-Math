#include <igraph/igraph.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

float f(int d, float d_mean, float th)
{
    float c = log(2.0);
    return 1.0 - exp(-c * (th * d / d_mean + (1.0 - th)));
}

float d_mean(igraph_t *graph)
{
    return 2.0 * igraph_ecount(graph) / (float) igraph_vcount(graph);
}

igraph_integer_t d(igraph_t *graph, igraph_integer_t v)
{
    igraph_vector_t res;
    igraph_vs_t vs;

    igraph_vector_init(&res, 1);
    igraph_vs_1(&vs, v);

    igraph_degree(graph, &res, vs, IGRAPH_ALL, IGRAPH_LOOPS); 
    igraph_integer_t d_v = VECTOR(res)[0];

    igraph_vs_destroy(&vs);
    igraph_vector_destroy(&res);
    return d_v;
}

void iterate(igraph_t *graph, float th)
{
    igraph_integer_t x, y, z, xy;
    
    xy = rand() % (int) igraph_ecount(graph);
    igraph_edge(graph, xy, &x, &y);

    //flip increasing orientation with pr 1/2
    if(rand() % 2)
    {
        igraph_integer_t buffer = y;
        y = x;
        x = buffer;
    }

    //condition to start while loop
    z = x;

    while((int) z == (int) x || (int) z == (int) y)
    {
        z = rand() % (int) igraph_vcount(graph);
    }

    if(d(graph, x) < 1 || d(graph, y) < 1 || d(graph, z) < 0)
    {
        
        exit(1);
    }

    int d_z = d(graph, z);
    if(1.0 * rand() / RAND_MAX < f(d_z, d_mean(graph), th))
    {
        igraph_es_t es;

        igraph_es_1(&es, xy);
        igraph_delete_edges(graph, es);
        igraph_es_destroy(&es);

        igraph_add_edge(graph, (int)x, (int)z);
        
    } 
}

void main()
{
    unsigned int seed = (unsigned int)time(NULL);
    srand(seed);

    igraph_t *graph;
    igraph_erdos_renyi_game(graph, IGRAPH_ERDOS_RENYI_GNM, 10, 20,
                             IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);

    int i;
    for(i = 0; i < pow(10, 5); i++)
    {
        iterate(graph, .5); 
    }

    igraph_write_graph_edgelist(graph, stdout);
    igraph_destroy(graph);
}
