#include <igraph/igraph.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_I 10000000000
#define MULTIPLE 1//100000 //iterations per vertex until stable
#define ITERATIONS 100000000 //iterations until stable
#define TRIALS_PER_GRAPH 100
#define TRIALS_PER_N 1
#define DEGREE_DIST 0 //record degree distribution?

#define MIN 300
#define MAX 300
#define STEP 100

#define TESTING 1	//use to test different multiples
#define PRINTLOTS 0 //to determine multiple by continuely running
#define USE_ITER 0  //(0) wait until a certain iterations per node
					//(1) wait until a certain number of iterations
					//until you test to see if it's stable

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

/*don't needs this.  use igraph_average_path_length()
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
*/


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

/*  This is using clusters
double get_pw_distance(igraph_t *graph){
    igraph_integer_t no;
	igraph_vector_t membership, csize;
	igraph_vector_init(&membership, 1);
	igraph_vector_init(&csize, 1);
	//TODO: use pairwise distance instead of diameter
	igraph_clusters(graph, &membership, &csize, &no, IGRAPH_WEAK);
	if(VECTOR(membership)[0] == VECTOR(membership)[1]){
		printf("they're the same!\n");
	} else {
		printf("they're different\n");
	}
	int t;
	printf("I think the LC is component %f", VECTOR(csize)[1]);
	
	for(t =0; t < 800; t++){
		printf("vertex %d belongs to component %f", t, VECTOR(membership)[t]);
	}
	igraph_vector_destroy(&membership);
	igraph_vector_destroy(&csize);
	return 0.0;
} */

double get_pw_distance(igraph_t *graph, int n){
	igraph_vector_ptr_t components;
	igraph_vector_ptr_init(&components, 1);
	//WARNING: assumes LC > half
	igraph_decompose(graph, &components, IGRAPH_WEAK, -1, n/2);
	igraph_t * buf, * largest_component;
	int max_size = 0, buf_size = 0;
	igraph_real_t pwd;
	int i;
	for(i = 0; i < igraph_vector_ptr_size(&components); i++){
		buf = (igraph_t*) (igraph_vector_ptr_e(&components, i));
		buf_size = igraph_vcount(buf);
		if (buf_size > max_size){
			max_size = buf_size;
			largest_component = buf;
		}
	}
	igraph_average_path_length(largest_component, &pwd, 0, 0);
	igraph_vector_ptr_destroy_all(&components);
	return (double) pwd;
}

double procedure(igraph_t *graph, double *opinions, int n, int m, int D,
    int alpha, int interval, int multiple, int dd)
{
    int i, j = 0, k, record = 0, trials = TRIALS_PER_GRAPH;
    int data[trials * n];
    double pw_distance_sum = 0.0, buf = 0.0;

    for(i = 0; i < MAX_I; i++)
    {
#if TESTING
		if(i % (ITERATIONS/10) == 0 && i != 0 && !record){
			printf("%d percent \n", (int)((double)i / (double)ITERATIONS * 100));
		}
#endif
        if(i % interval == 0 && i != 0)
        {
#if PRINTLOTS
			buf = get_pw_distance(graph, n);
			printf("%d: %.5g\n", i, buf);
#endif

            if(!record){
#if USE_ITER
				if(i > ITERATIONS){
#else
                if(i > multiple*n && multiple != 0){ //multiple = 0  to never record (debugging)
					printf("****************** RECORDING ******************\n");
#endif					
                    record = 1;
                }
            } else {
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
					buf = get_pw_distance(graph, n);
#if TESTING
					printf("%d: %.5g\n", i, buf);
#endif
                    pw_distance_sum += buf;
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

    return pw_distance_sum / trials;
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

    double pw_distance_sum;
    char outstring[1000];
	outstring[0] = '\0';
	strcat(outstring, "n\tpair-wise distance\n");
#if !TESTING
	printf("n\tpair-wise distance\n");
#endif

    int trials = TRIALS_PER_N;
    int multiple = MULTIPLE; //iterations per vertex until stable
	int degreeDistro = DEGREE_DIST;

    for(n = MIN; n <= MAX; n += STEP)
    {
        m = 2 * n;

        int i;
        pw_distance_sum = 0;

        for(i = 0; i < trials; i++)
        {
            igraph_t graph;
            igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNM, n, m,
                IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);

            double opinions[n][D];
            generate_opinions(n, D, &opinions[0][0]);

            pw_distance_sum += procedure(&graph, &opinions[0][0], n, m,
                D, alpha, interval, multiple, degreeDistro)/trials;
        }

        char buffer[100];
        sprintf(buffer, "%d\t%g\n", n, pw_distance_sum);// (double) trials);
#if TESTING
		printf("****************************************\n");
        printf("%s", buffer);
		printf("****************************************\n");
#else
		printf("%s", buffer);
#endif
        strcat(outstring, buffer);
    }

    printf("\n%s\n", outstring);
	FILE *pfile = NULL;
	char *filename = "output.dat";
    pfile = fopen(filename, "w");
    if(pfile == NULL)
	{
		printf("Error opening %s for writing. Program terminated.", filename);
	}
	/*
	int i = 0;
    for(i = 0 ; i < sizeof outstring/sizeof outstring[0] ; i++)
    	fputs(outstring[i], pfile);
	*/
	fputs(outstring, pfile);
    fclose(pfile);
}
