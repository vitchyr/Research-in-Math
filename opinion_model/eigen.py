import scipy
import numpy as np
import scipy.linalg

import model

if __name__ == '__main__':
    n = 500
    b = .000006662 

    ticks = 1000

    D = 1
    alpha = 2

    type_ids = np.ndindex(tuple([ticks]* D * 2))
    M = np.zeros([ticks] * D * 2)
    
    for index in type_ids:
        i = index[:D]
        j = index[D:]

        if i != j:
            pos_i = [float(_i) / (ticks - 1) for _i in i] 
            pos_j = [float(_j) / (ticks - 1) for _j in j]

            M[i, j] = b / (b + model.distance(None, pos_i, pos_j)) 

    eigvals = scipy.linalg.eigvals(M) 
    print max(eigvals)
