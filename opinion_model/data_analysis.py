import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math

def function(x):
    return x

filename = "opDiameter_4k_1D_2alpha_200min_4700max_5times_5size.dat"
f = open(filename, 'r')

headers = f.readline().replace('\n','').split('\t')
x = []
y = []

for line in f:
    datum = line.replace('\n','').split('\t')
    x.append(function(int(datum[0])))
    y.append(float(datum[1]))

f.close()

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

plt.scatter(x,y, label="Observed")
plt.ylabel(headers[1])
plt.xlabel(headers[0])

##coefs = np.lib.polyfit(x, y, 1)
##fit_y = np.lib.polyval(coefs, x)
##plt.plot(x, fit_y, 'b-', label="Line of best fit") # label="Correlation: %0.5f" % (r_value))

##plt.axis([0,5500, 0,700000])
##ax = plt.gca()    
##ax.set_autoscale_on(False)
plt.legend(loc=4)
plt.figtext(.5,0.005,"Correlation: %0.5f" % r_value, fontsize=12, ha='center')

plt.savefig(filename[:-4]+".pdf")
