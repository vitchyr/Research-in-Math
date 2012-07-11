#include <igraph/igraph.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

#include "model.h"

void dd(int *distro, igraph_t *graph, int m)
{
    int i;
    for(i = 0; i <= m; i++)
    {
        distro[i] = 0;
    }

    igraph_vector_t deg_vector;
    igraph_vector_init(&deg_vector, 1);

    igraph_vs_t vs;
    igraph_vs_all(&vs);

    igraph_degree(graph, &deg_vector, vs, IGRAPH_ALL, 1);

    int deg;
    for(i = 0; i < igraph_vector_size(&deg_vector); i++)
    {
        deg = VECTOR(deg_vector)[i];
        distro[deg] = 1 + distro[deg]; 
    }

    igraph_vs_destroy(&vs);
    igraph_vector_destroy(&deg_vector);
}

int sum_array(double a[], int num_elements){
    int i, sum=0;
    for (i=0; i<num_elements; i++){
        sum = sum + a[i];
    }
    return(sum);
}

void expected_dd(double *expectedDistro, int d_mean, int n, int m, double th){
    int i;
    for(i = 0; i < n; i++){
        if(i==0){
            expectedDistro[i] = 1.0;
        } else if (i == 1){
            expectedDistro[i] = 2.0*m / (2.0*m + n) * f(0, d_mean, th);
        } else {
            expectedDistro[i] = 2.0*m / i * ((f(i-1, d_mean, th)/(2.0*m+n) 
            + (i-1)/(2.0*m))*expectedDistro[i-1]
            - f(i-2, d_mean, th)/(2.0*m+n) * expectedDistro[i-2]);
        }
    }
    int sum = sum_array(expectedDistro, sizeof(expectedDistro)/sizeof(double));
    for(i = 0; i < n; i++){
        expectedDistro[i] = (int)(n*expectedDistro[i]/sum);
    }
}

void dd_procedure(int n, int m, int times, double th_min, double th_step, double th_max)
{
    int n_lines = n * (int) ((th_max - th_min) / th_step);

    if(n_lines < n)
    {
        n_lines = n;
    }

    int max_line_length = 200;
    char outstring[n_lines * max_line_length];
    strcpy(outstring, "th\tdeg\tobserved freq\texpected freq\n");

    igraph_t graph;
    int distro[m + 1];
    double expectedDistro[n];

    double th;
    for(th = th_min; th <= th_max + th_step/10; th += th_step)
    {
        printf("th = %f\n", th);
        igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNM, n, m,
            IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);
        iterate_many(&graph, th, times);    

        dd(distro, &graph, n); 
        expected_dd(expectedDistro, get_d_mean(&graph), n, m, th);

        int i;
        for(i = 0; i <= m; i++)
        {
            char buffer[max_line_length]; 
            sprintf(buffer, "%f\t%d\t%d\n", th, i, distro[i]);
            strcat(outstring, buffer);
        }
    }

    igraph_destroy(&graph);

    char filename[200];
    sprintf(filename, "dd_%d_%d_%d_%d%%_%d%%_%d%%_%d.dat", n, m, times,
        (int) (100 * th_min), (int) (100 * th_step), (int) (100 * th_max), 3);
    
    FILE *outfile = fopen(filename, "w");
    fputs(outstring, outfile);
    fclose(outfile);
}

double get_lc_frac(igraph_t *graph)
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

double stats_procedure_loop(int n, int m, int times, double th, int stats_size)
{
    int i;
    double lc_frac_sum = 0.0;
    
    for(i = 0; i < stats_size; i++)
    {
        igraph_t graph;

        igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNM, n, m,
            IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);
        iterate_many(&graph, th, times);    

        lc_frac_sum += get_lc_frac(&graph);
    }

    return lc_frac_sum / (double) stats_size;
}

void stats_procedure(int n, int m, int times, double th_min,
    double th_step, double th_max, int stats_size)
{
    int n_lines = n * (int) ((th_max - th_min) / th_step);
    int max_line_length = 200;
    char outstring[n_lines * max_line_length];
    strcpy(outstring, "th\tlc_frac\n");

    double th, lc_frac;
    for(th = th_min; th <= th_max + .001; th += th_step)
    {
        printf("th = %f\n", th);
        lc_frac = stats_procedure_loop(n, m, times, th, stats_size);    

        char buffer[max_line_length]; 
        sprintf(buffer, "%f\t%f\n", th, lc_frac);
        strcat(outstring, buffer);
    }

    char filename[200];
    sprintf(filename, "stats_%d_%d_%d_%d%%_%d%%_%d%%_%d.dat", n, m, times,
        (int) (100 * th_min), (int) (100 * th_step),
        (int) (100 * th_max), stats_size);
    
    FILE *outfile = fopen(filename, "w");
    fputs(outstring, outfile);
    fclose(outfile);
}

void main(int argc, char *argv[])
{
    int n, m, times, stats_size = 0;
    double th_min, th_step, th_max;

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
        stats_procedure(n, m, times, th_min, th_step, th_max, stats_size);
    }
}
