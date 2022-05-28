import os
import argparse
import timeit
from utils.generate import generate

if __name__ == '__main__':
    if not os.path.isdir('images/'):
        imports = 'from __main__ import generate'
        elapsed = timeit.timeit('generate()', imports, number=1)
        print(f'Generated images in {elapsed:.5f}s')
