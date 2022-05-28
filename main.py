import os
import argparse
import timeit
from utils.generate import generate

parser = argparse.ArgumentParser(description='Parameters')
parser.add_argument('--noise', action='store_true',
                    help='Specify whether to generate images with noise or not')
args = parser.parse_args()
noise = args.noise
if __name__ == '__main__':
    if not os.path.isdir('images/'):
        imports = 'from __main__ import noise, generate'
        elapsed = timeit.timeit('generate(noise)', imports, number=1)
        print(f'Generated images in {elapsed:.5f}s')
