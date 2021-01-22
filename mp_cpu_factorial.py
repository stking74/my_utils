import time
from multiprocessing import Pool

def factorial(n):
    if n == 1: return 1
    else: return n * factorial(n-1)

pool = Pool(12)

ti = time.time()
result = pool.map(factorial, [200 for i in range(100000)])
print(time.time() - ti)
