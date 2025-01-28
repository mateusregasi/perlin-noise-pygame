import numpy as np
a = [[1,2,3],[4,5,6],[7,8,9]]
a = np.array(a)

def f(a, v):
    return a+v

print(f(a,10))