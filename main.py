import os
import argparse
import time
from utils.generate import generate
from utils.kmeans import kmean_processes

if __name__ == '__main__':
    if not os.path.isdir('images/'):
        generate()
    start = time.time()
    kmean_processes()
    end = time.time()
    print(end - start)
