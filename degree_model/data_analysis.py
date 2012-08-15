import matplotlib.pyplot as plt
import math

xlist = []
ylist = []
filename = ""

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
    xlist.append(x)
    ylist.append(y)

    if number == 0:
        plt.scatter(x,y, c='r', marker='o', label="theta = {0}".format(formatString))
    elif number == 5:
        plt.scatter(x,y, c='g', marker='s', label="theta = {0}".format(formatString))
    else:
        plt.scatter(x,y, c='b', marker='^', label="theta = {0}".format(formatString))
    plt.xlabel(headers[0])
    plt.ylabel(headers[1])

    ##plt.axis([0,5500, 0,700000])
    ##ax = plt.gca()    
    ##ax.set_autoscale_on(False)
plt.legend(loc=4)

plt.savefig("data/degree_model_lc_2000n.pdf")

