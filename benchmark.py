# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:13:46 2019

@author: tyler
"""



from multiprocessing import Pool
import numpy as np
import time

def apply_polynomial(x, c):
    '''
    Applies nth order polynomial to input array x. n is equal to len(c) - 1.

    when c = (1, -2, 3), function is equivalent to:
        f(x) = 3*x**2 - 2*x + 1

    Input:
    --------
        x : array-like
            data to be evaluated with polynomial
        c : array-like
            polynomial coefficients in ascending polynomial order
    '''
    import numpy as np
    x = np.asarray(x)
    y = np.empty_like(x, dtype=np.float64)
    for i, v in enumerate(x):
        y_i = 0
        for idx, coeff in enumerate(np.flip(c)):
            y_i += (v**idx)*coeff
        y[i] = y_i
    return y

def parse_row(row, rownumber):
    newrow = np.empty_like(row)
    j = len(row)
    for k, cell in enumerate(row):
        newrow[k] = (j*rownumber) + k
    return newrow

n_cores = 4

print('Performing single core tests...')
x = []
y = []
for i in range(6, 15):
    i = 2**i
    ti = time.time()
    arr = np.arange(i*i, dtype=np.uint64).reshape(i,i)
    for j, row in enumerate(arr):
        arr[j] = parse_row(row, j)
    dt = time.time() - ti
    print(i, dt)
    x.append(i)
    y.append(dt)
    time.sleep(1)
    
# Let's take the randomness out of random numbers (for reproducibility)
np.random.seed(0)

size = 4096
A, B = np.random.random((size, size)), np.random.random((size, size))
C, D = np.random.random((size * 128,)), np.random.random((size * 128,))
E = np.random.random((int(size / 2), int(size / 4)))
F = np.random.random((int(size / 2), int(size / 2)))
F = np.dot(F, F.T)
G = np.random.random((int(size / 2), int(size / 2)))

# Matrix multiplication
N = 20
t = time()
for i in range(N):
    np.dot(A, B)
delta = time() - t
print('Dotted two %dx%d matrices in %0.2f s.' % (size, size, delta / N))
del A, B

# Vector multiplication
N = 5000
t = time()
for i in range(N):
    np.dot(C, D)
delta = time() - t
print('Dotted two vectors of length %d in %0.2f ms.' % (size * 128, 1e3 * delta / N))
del C, D

# Singular Value Decomposition (SVD)
N = 3
t = time()
for i in range(N):
    np.linalg.svd(E, full_matrices = False)
delta = time() - t
print("SVD of a %dx%d matrix in %0.2f s." % (size / 2, size / 4, delta / N))
del E

# Cholesky Decomposition
N = 3
t = time()
for i in range(N):
    np.linalg.cholesky(F)
delta = time() - t
print("Cholesky decomposition of a %dx%d matrix in %0.2f s." % (size / 2, size / 2, delta / N))

# Eigendecomposition
t = time()
for i in range(N):
    np.linalg.eig(G)
delta = time() - t
print("Eigendecomposition of a %dx%d matrix in %0.2f s." % (size / 2, size / 2, delta / N))

p = np.polyfit(x, y, 2)
