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

double procedure(igraph_t *graph, double *opinions, int n, int m, int D,
    int alpha, int interval, int multiple, int dd)
{
    int i, j = 0, k, record = 0, trials = 100;
    int data[trials * n];
    double diameter = 0.0;
    igraph_integer_t diameter_tmp;

    for(i = 0; i < 1000000000; i++)
    {
        if(i % interval == 0 && i != 0)
        {
            //TODO: uncomment to determine multiple
            //igraph_diameter(graph, &diameter_tmp, 0, 0, 0, 1, 1);
            //printf("%d // %g: ", i, diameter_tmp);

            if(!record)
            {
                //char input = getchar();

                /*if(input == 'q')
                {
                    break;
                }*/

                if(i > multiple*n)
                {
                    record = 1;
                }
            } else
            {
                if(j == trials)
                {
                    break;
                }

                if(dd)
                {
                    igraph_vector_t deg_vector;
                    igraph_vector_init(&deg_vector, 1);

                    igraph_vs_t vs;
                    igraph_vs_all(&vs);

                    igraph_degree(graph, &deg_vector, vs, IGRAPH_ALL, 1);

                    for(k = 0; k < igraph_vector_size(&deg_vector); k++)
                    {
                        data[j*n + k] = VECTOR(deg_vector)[k];
                    }

                    igraph_vs_destroy(&vs);
                    igraph_vector_destroy(&deg_vector);
                } else {
                    igraph_diameter(graph, &diameter_tmp, 0, 0, 0, 1, 1);
                    diameter += ((double)diameter_tmp) / trials;
                }

                j++;
            }
        }

        iterate(graph, opinions, n, m, D, alpha); 
    }

    if(dd)
    {
        char outstring[3 * n * trials];
        for(i = 0; i < trials * n; i++)
        {
            char buffer[10];
            sprintf(buffer, "%d,", data[i]);
            strcat(outstring, buffer);
        }

        char filename[200];
        sprintf(filename, "opddc_%d_%d.dat", D, alpha);
        
        FILE *outfile = fopen(filename, "w");
        fputs(outstring, outfile);
        fclose(outfile);
    } 

    return diameter;
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

    double diameter;
    char outstring[1000];

    //TODO: set trials and multiple
    int trials = 10;
    int multiple = 10000;

    //TODO: set n range and increment
    for(n = 800; n <= 1000; n += 100)
    {
        m = 2 * n;

        int i;
        diameter = 0;

        for(i = 0; i < trials; i++)
        {
            igraph_t graph;
            igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNM, n, m,
                IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);

            double opinions[n][D];
            generate_opinions(n, D, &opinions[0][0]);

            diameter += procedure(&graph, &opinions[0][0], n, m,
                D, alpha, interval, multiple, 0) / trials;
        }

        char buffer[100];
        sprintf(buffer, "%d\t%g\n", n, diameter);
        printf("%s", buffer);
        strcat(outstring, buffer);
    }

    //printf("\n%s\n", outstring);
}
