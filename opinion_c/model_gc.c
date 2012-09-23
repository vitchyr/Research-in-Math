#include <igraph/igraph.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

double d(double *opinions, int D, igraph_integer_t x, igraph_integer_t y)
{
    int i;
    double total = 0.0;

    for(i = 0; i < D; i++)
    {
        total += fabs(opinions[(size_t)(x * D + i)] -
            opinions[(size_t)(y * D + i)]);
    }

    return total;
}

double mean_distance(igraph_t *graph, double *opinions, int m, int D)
{
    igraph_integer_t x, y, edge;
    double total;

    for(edge = 0.0; edge < m; edge++)
    {
        igraph_edge(graph, edge, &x, &y);
        total += d(opinions, D, x, y);
    }

    return total / (double) m;
} 

void iterate(igraph_t *graph, double *opinions, int n, int m, 
    int D, int alpha)
{
    igraph_integer_t x, y, z, xy;
    
    xy = rand() % m;
    igraph_edge(graph, xy, &x, &y);

    //flip increasing orientation with pr 1/2
    if(rand() % 2)
    {
        igraph_integer_t buffer = y;
        y = x;
        x = buffer;
    }

    z = x;
    igraph_vector_t neighbors;
    igraph_vector_init(&neighbors, 1);
    igraph_neighbors(graph, &neighbors, x, IGRAPH_ALL);

    while(abs(z - x) < .1 || abs(z - y) < .1 ||
        igraph_vector_contains(&neighbors, z))
    {
        z = rand() % n;
    }

    igraph_vector_destroy(&neighbors);

    double d_xy = d(opinions, D, x, y);
    double d_xz = d(opinions, D, x, z);

    double mh_factor = 1.0;
    if(alpha == 2)
    {
        if(d_xy / d_xz < 1)
        {
            mh_factor = d_xy / d_xz;
        }
    }

    if(((double) rand()) / RAND_MAX < (1.0 / D) * d_xy * mh_factor)
    {
        igraph_es_t es;

        igraph_es_1(&es, xy);
        igraph_delete_edges(graph, es);
        igraph_es_destroy(&es);

        igraph_add_edge(graph, x, z);
    } 
}

void generate_opinions(int n, int D, double *opinions)
{
    int i, j;

    for(i = 0; i < n; i++)
    {
        for(j = 0; j < D; j++)
        {
            opinions[(size_t)(i*D + j)] = ((double) rand()) / RAND_MAX;
        }
    }
}

double get_gc_frac(igraph_t *graph)
{
    igraph_vector_ptr_t components;
    igraph_vector_ptr_init(&components, 1);

    //ignore lone vertices
    igraph_decompose(graph, &components, IGRAPH_WEAK, -1, 2);

    igraph_t *component;
    int i, max_size = 0;
    for(i = 0; i < igraph_vector_ptr_size(&components); i++)
    {
        component = (igraph_t *)igraph_vector_ptr_e(&components, i);
        if(igraph_vcount(component) > max_size)
        {
            max_size = igraph_vcount(component);
        }
    }

    igraph_decompose_destroy(&components);
    return (double) max_size / (double) igraph_vcount(graph);
} 

double procedure(igraph_t *graph, double *opinions, int n, int m, int D,
    int alpha, int interval, int multiple, int dd)
{
    int i, j = 0, k, record = 0, trials = 100;
    double gc_frac = 0.0;

    for(i = 0; i < 1000000000; i++)
    {
        if(i % interval == 0 && i != 0)
        {
            //UNCOMMENT
            //printf("%d // %g: ", i, mean_distance(graph, opinions, m, D));

            if(!record)
            {
                if(i > multiple*m)
                {
                    record = 1;
                }
            } else
            {
                if(j == trials)
                {
                    break;
                }

                gc_frac += get_gc_frac(graph) / trials;
                j++;
            }
        }

        iterate(graph, opinions, n, m, D, alpha); 
    }

    return gc_frac;
}

void main(int argc, char *argv[])
{
    int n, m, D, alpha, interval;

    if(argc == 4)
    {
        //n = atoi(argv[1]);
        //m = atoi(argv[2]);
        D = atoi(argv[1]);
        alpha = atoi(argv[2]);
        interval = atoi(argv[3]);
    } else {
        printf("Syntax: ./model D alpha interval\n");
        printf("Exiting...\n");
        return;
    }

    unsigned int seed = (unsigned int)time(NULL);
    srand(seed);

    double gc_frac;
    int trials = 10;
    int multiple = 10000;
    n = 1000;
    double k_mean;

    for(k_mean = .6; k_mean <= 8.0; k_mean += .2)
    {
        m=(int) (.5 * k_mean * (double) n);

        int i;
        gc_frac = 0.0;

        for(i = 0; i < trials; i++)
        {
            igraph_t graph;
            igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNM, n, m,
                IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);

            double opinions[n][D];
            generate_opinions(n, D, &opinions[0][0]);

            gc_frac += procedure(&graph, &opinions[0][0], n, m,
                D, alpha, interval, multiple, 0) / trials;
        }

        char buffer[100];
        sprintf(buffer, "%g\t%g\n", k_mean, gc_frac);
        printf("%s", buffer);
        //strcat(outstring, buffer);
    }

    //printf("\n%s\n", outstring);
}
