#include <igraph/igraph.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

#include "model.h"

void dd(int *distro, igraph_t *graph, int n)
{
    int i;
    for(i = 0; i < n; i++)
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

void dd_procedure(int n, int m, int times, float th_min, float th_step, float th_max)
{
    int n_lines = n * (int) ((th_max - th_min) / th_step);
    int max_line_length = 200;
    char outstring[n_lines * max_line_length];
    strcpy(outstring, "th\tdeg\tfreq\n");

    igraph_t graph;
    int distro[n];

    float th;
    for(th = th_min; th <= th_max + .001; th += th_step)
    {
        igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNM, n, m,
            IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);
        iterate_many(&graph, th, times);    

        dd(distro, &graph, n); 

        int i;
        for(i = 0; i < n; i++)
        {
            char buffer[max_line_length]; 
            sprintf(buffer, "%f\t%d\t%d\n", th, i, distro[i]);
            strcat(outstring, buffer);
        }

    }

    igraph_destroy(&graph);

    char filename[200];
    sprintf(filename, "dd_%d_%d_%d_%d%%_%d%%_%d%%.dat", n, m, times,
        (int) (100 * th_min), (int) (100 * th_step), (int) (100 * th_max));
    
    FILE *outfile = fopen(filename, "w");
    fputs(outstring, outfile);
    fclose(outfile);
}

struct stats_task_result {
    float lc_frac;
    int lc_diameter;
    int n_components;
};

struct stats_task_descriptor {
    int n;
    int m;
    int times;
    float th;
    struct stats_task_result res;
};

void * stats_task(void *ptr)
{
    struct stats_task_descriptor *desc = (struct stats_task_descriptor * )ptr;

    desc->res.lc_frac = .01;
    desc->res.lc_diameter = 2;
    desc->res.n_components = 5;

    //igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNM, n, m,
      //  IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);
    //iterate_many(&graph, th, times);    
}

void stats_procedure_loop(struct stats_task_result *result_array,
    int n, int m, int times, float th, int stats_size)
{
    int n_threads = 4;
    pthread_t threads[n_threads];
    int thread_id, task_count;

    struct stats_task_descriptor desc_array[n_threads];

    task_count = 0;
    while(task_count != stats_size)
    {
        for(thread_id = 0; thread_id < n_threads; thread_id++)
        {
            desc_array[thread_id].n = n;
            desc_array[thread_id].m = m;
            desc_array[thread_id].times = times;
            desc_array[thread_id].th = th;

            if(task_count < stats_size)
            {
                pthread_create(&threads[thread_id], NULL, stats_task,
                    (void *) &desc_array[thread_id]);  
                task_count++;
            } 
        }


        for(thread_id = 0; thread_id < n_threads; thread_id++)
        {
            pthread_join(threads[thread_id], NULL);

            result_array[task_count - thread_id - 1] =
                desc_array[thread_id].res;
        }
    }
}

void stats_procedure(int n, int m, int times, float th_min,
    float th_step, float th_max, int stats_size)
{
    int n_lines = n * (int) ((th_max - th_min) / th_step);
    int max_line_length = 200;
    char outstring[n_lines * max_line_length];
    strcpy(outstring, "th\tlc_frac\tlc_diameter\tn_components\n");


    struct stats_task_result result_array[stats_size];
    float th;
    for(th = th_min; th <= th_max + .001; th += th_step)
    {
        stats_procedure_loop(result_array, n, m, times, th, stats_size);    
        int i;
        for(i = 0; i < stats_size; i++)
        {
            printf("%f\n", result_array[i].lc_frac);
            //char buffer[max_line_length]; 
            //sprintf(buffer, "%f\t%d\t%d\n", th, i, distro[i]);
            //strcat(outstring, buffer);
        }

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
        stats_procedure(n, m, times, th_min, th_step, th_max, stats_size);
    }
}
