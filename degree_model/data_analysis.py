import matplotlib.pyplot as plt
import math

for number in range(0,15,5):
    formatString = "%0.1f" % (number/10.0)
    filename = "data/stats_2000n_"+formatString+"00000th_"+str(int(number/10) + 1)+"00000times_0.600000kmin_0.200000kstep_2.000000kmax_10statsize.dat"
    f = open(filename, 'r')

    headers = f.readline().replace('\n','').split('\t')
    x = []
    y = []

    for line in f:
        datum = line.replace('\n','').split('\t')
        x.append(float(datum[0]))
        y.append(float(datum[1]))
    
    f.close()

    if number == 0:
        plt.scatter(x,y, c='r', marker='s', label="theta = {0}".format(formatString))
    elif number == 5:
        plt.scatter(x,y, c='g', marker='^', label="theta = {0}".format(formatString))
    else:
        plt.scatter(x,y, c='b', marker='o', label="theta = {0}".format(formatString))

plt.title("Size of Largest Component: theta = 0, 0.5, 1")
plt.xlabel("Average Degree")
plt.ylabel("Fraction of Vertices in Largest Component")
##plt.xlim(0, 2)
##plt.ylim(0,1)
plt.legend(loc=4)
plt.savefig("data/degree_model_lc_2000n.pdf")

