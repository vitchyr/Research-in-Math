import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math

def function(x):
    return math.log(x)
##    return x

filename1 = "opPairwise_4k_1D_2alpha_200min_800max_10000times_1size.dat"
f1 = open(filename1, 'r')

headers = f1.readline().replace('\n','').split('\t')
x1 = []
y1 = []

for line in f1:
    datum = line.replace('\n','').split('\t')
    x1.append(function(int(datum[0])))
    y1.append(float(datum[1]))

f1.close()

##filename2 = "opPairwise_4k_2D_2alpha_200min_1200max_1000times_1size.dat"
##f2 = open(filename2, 'r')
##
##headers = f2.readline().replace('\n','').split('\t')
##x2 = []
##y2 = []
##
##for line in f2:
##    datum = line.replace('\n','').split('\t')
##    x2.append(function(int(datum[0])))
##    y2.append(float(datum[1]))
##
##f2.close()

#Fitting lines:
slope, intercept, r_value, p_value, std_err = stats.linregress(x1,y1)
coefs1 = np.lib.polyfit(x1, y1, 1)
fit_y1 = np.lib.polyval(coefs1, x1)
plt.plot(x1, fit_y1, 'b-')

##slope, intercept, r_value, p_value, std_err = stats.linregress(x2,y2)
##coefs2 = np.lib.polyfit(x2, y2, 1)
##fit_y2 = np.lib.polyval(coefs2, x2)
##plt.plot(x2, fit_y2, 'g-')

#Labels:
plt.scatter(x1,y1, c='b', label=r'$\alpha$ = 1')
##plt.scatter(x2,y2, c='g', label=r'$\alpha$ = 2')
plt.ylabel(headers[1])
##plt.xlabel(headers[0])
plt.xlabel("$Log(" + headers[0] +")$")
#TODO: name plot title
plt.title(r'Mean Pair-Wise Distance in Giant Component, d = 1, $\alpha$=2')
##plt.legend(loc=4)

#TODO: name save files
plt.savefig("figure6_test.pdf")
##plt.savefig(filename1[:-4] + ".pdf")
