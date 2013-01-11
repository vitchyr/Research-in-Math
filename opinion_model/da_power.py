import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import math

def function(x, a, b, c):
    return a*np.exp(b*x) + c

filename1 = "output.dat"
f1 = open(filename1, 'r')

headers = f1.readline().replace('\n','').split('\t')
x1 = []
y1 = []

for line in f1:
    datum = line.replace('\n','').split('\t')
    x1.append(function(int(datum[0])))
    y1.append(float(datum[1]))

f1.close()

#Fitting power law:
popt, pcov = curve_fit(function, x, y);
print "popt: " + popt
print "pcov: " + pcov

#Labels:
plt.scatter(x1,y1, c='b', label=r'$\alpha$ = 1, exponent = ?')
plt.ylabel(headers[1])
plt.xlabel(headers[0])
#TODO: name plot title
plt.title(r'Mean Pair-Wise Distance in Giant Component, d = 1, $\alpha$=2')
##plt.legend(loc=4)

#TODO: name save files
plt.savefig("figure6_test.pdf")
