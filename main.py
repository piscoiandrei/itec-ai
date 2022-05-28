import os
import argparse
import timeit
from utils.generate import generate
from utils.kmeans import compute_kmeans

if __name__ == '__main__':
    if not os.path.isdir('images/'):
        imports = 'from __main__ import generate'
        elapsed = timeit.timeit('generate()', imports, number=1)
        print(f'Generated images in {elapsed:.2f}s')
    kmean_time = timeit.timeit('compute_kmeans()',
                               'from __main__ import compute_kmeans'
                               , number=1)
    print(f'Applied K-mean in {kmean_time:.2f}s')
