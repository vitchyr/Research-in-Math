#include <igraph/igraph.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "model.h"

double f(int d, double d_mean, double th)
{
    return th * pow((double) d + 1.0, 3) + (1.0 - th) * pow(d_mean + 1.0, 3);
}

double d_mean(igraph_t *graph)
{
    return 2.0 * igraph_ecount(graph) / (double) igraph_vcount(graph);
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

igraph_integer_t all_degrees(igraph_t *graph, igraph_vector_t *degrees)
{
    igraph_vs_t vs;
    igraph_vs_all(&vs);

    igraph_degree(graph, degrees, vs, IGRAPH_ALL, IGRAPH_LOOPS); 
    igraph_vs_destroy(&vs);
}

double getDenom(igraph_t *graph, igraph_vector_t *degrees, double theta){
    double denom = 0;
    double dMean = d_mean(graph);
    int i;
    for(i = 0; i < igraph_vector_size(degrees); i++){
        denom += f(VECTOR(*degrees)[i], dMean, theta);
    }
    return denom;
}

void iterate(igraph_t *graph, double th)
{
    igraph_integer_t x, y, z = -1.0, xy;
    
    xy = rand() % (int) igraph_ecount(graph);
    igraph_edge(graph, xy, &x, &y);

    //flip increasing orientation with pr 1/2
    if(rand() % 2)
    {
        igraph_integer_t buffer = y;
        y = x;
        x = buffer;
    }

    igraph_vector_t degrees;
    igraph_vector_init(&degrees, 1); 
    all_degrees(graph, &degrees);

    double random = 1.0 * rand() / RAND_MAX;
    int w;
    double total = 0.0;
    double denom = getDenom(graph, &degrees, th);
    for(w = 0; w < igraph_vector_size(&degrees); w++)
    {
        if(w != (int) x && w != (int) y)
        {
            total += f(VECTOR(degrees)[w], d_mean(graph), th) / denom; 

            if(random < total)
            {
                z = (igraph_integer_t) w;
                break;
            }
        }
    }

    igraph_vector_destroy(&degrees);

    if(z > -.5)
    {
        igraph_es_t es;

        igraph_es_1(&es, xy);
        igraph_delete_edges(graph, es);
        igraph_es_destroy(&es);

        igraph_add_edge(graph, x, z);
    } 
}

void iterate_many(igraph_t *graph, double th, int times)
{
    //double denom = getDenom(graph, th);
    int i;
    for(i = 0; i < times; i++)
    {
        iterate(graph, th); 
    }
}

