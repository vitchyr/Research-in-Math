import scipy
import numpy as np
import scipy.linalg

import model


def procedure(ticks):
    n = 500
    b = .000006662 
    D = 1
    alpha = 2

    n_types = ticks**D
    #print 'Number of types: {}'.format(n_types)
    M = np.zeros([ticks**D, ticks**D])
    registry = {}
    
    next_id = 0

    for index in np.ndindex(tuple([ticks] * D)):
        i = index[:D]
        registry[i] = next_id 
        next_id += 1

    for index in np.ndindex(tuple([ticks]* D * 2)):
        i = index[:D]
        j = index[D:]

        if i != j:
            pos_i = [float(_i) / (ticks - 1) for _i in i]
            pos_j = [float(_j) / (ticks - 1) for _j in j]

            M[registry[i], registry[j]] = .5 * n**2 / n_types**2 *\
                b / (b + model.distance(None, pos_i, pos_j)**alpha) 

    eigvals = scipy.linalg.eigvals(M) 
    return max(eigvals)

if __name__ == '__main__':
    print procedure(5000)
if __name__ == '__main__':
    print procedure(5000)
