import time
import statistics

def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)
    
n_cycles = 50

cycle_times = []
for i in range(n_cycles):
    ti = time.time()
    for i in range(10000):
        factorial(200)
    cycle_times.append(time.time() - ti)
    time.sleep(1)

mean_time = statistics.mean(cycle_times)
stdev_time = statistics.stdev(cycle_times)
rsd_time = stdev_time / mean_time * 100
print('Result of %i cycles:'%(n_cycles))
print('Mean (s): %f, RSD (%%): %f'%(mean_time, rsd_time))