#include <igraph/igraph.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

#include "model.h"

void dd(int *distro, igraph_t *graph)
{
    int i;
    for(i = 0; i < 20; i++)
    {
    distro[i] = i;
    }
}

void dd_procedure(int n, int m, int times, float th_min, float th_step, float th_max)
{
    int *distro;

    int n_lines = n * (int) ((th_max - th_min) / th_step);
    int max_line_length = 200;
    char outstring[n_lines * max_line_length];
    strcpy(outstring, "th\tdeg\tfreq\n");

    igraph_t graph;

    float th;
    for(th = th_min; th <= th_max + .001; th += th_step)
    {
        igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNM, n, m,
            IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);
        iterate_many(&graph, th, times);    

        int distro[n];
        dd(distro, &graph); 

        int i;
        for(i = 0; i < n; i++)
        {
            char buffer[max_line_length]; 
            sprintf(buffer, "%f\t%d\t%d\n", th, i, distro[i]);
            strcat(outstring, buffer);
        }
    }

    igraph_destroy(&graph);
    printf("%s\n", outstring);
}

void main(int argc, char *argv[])
{
    int n, m, times, stats_size = 0;
    float th_min, th_step, th_max;

    if(argc > 6)
    {
        n = atoi(argv[1]);
        m = atoi(argv[2]);
        times = atoi(argv[3]);
        th_min = atof(argv[4]);
        th_step = atof(argv[5]);
        th_max = atof(argv[6]);

        if(argc > 7)
        {
            stats_size = atoi(argv[7]);
        }
    } else {
        printf("Syntax: ./data_miner n m times th_min th_step th_max [stats_size]\n");
        printf("Exiting...\n");
        return;
    }

    unsigned int seed = (unsigned int)time(NULL);
    srand(seed);

    if(stats_size == 0)
    {
        dd_procedure(n, m, times, th_min, th_step, th_max);
    } else {

    }
}
